import streamlit as st
from api import api_get
from configure import OPENCAGE_KEY, GEONAMES_USERNAME, REST_COUNTRIES_URL, ALADHAN_URL

@st.cache_data(show_spinner=False)
def get_all_countries():
    data = api_get(REST_COUNTRIES_URL)
    if not isinstance(data, list):
        return {}
    countries = {
        c.get("name", {}).get("common"): c.get("cca2")
        for c in data if isinstance(c, dict) and c.get("cca2")
    }
    return dict(sorted(countries.items()))

@st.cache_data(show_spinner=False)
def get_cities_for_country(country_code):
    if not country_code:
        return []
    url = "https://secure.geonames.org/searchJSON"
    params = {
        "country": country_code,
        "featureClass": "P",
        "maxRows": 1000,
        "username": GEONAMES_USERNAME
    }
    data = api_get(url, params=params)
    if not data:
        return []
    cities = {place.get("name") for place in data.get("geonames", []) if place.get("name")}
    return sorted(cities)

def validate_city_country(city, country):
    if not city or not country:
        return False
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {"q": city, "key": OPENCAGE_KEY}
    geo = api_get(url, params=params)
    if not geo or geo.get("total_results", 0) == 0:
        return False
    return any(country.lower() in r.get("components", {}).get("country", "").lower()
               for r in geo.get("results", []))

def get_prayer_timings(city, country):
    params = {"city": city, "country": country, "method": 2}
    return api_get(ALADHAN_URL, params=params)
