import streamlit as st
import requests
from datetime import datetime
import pytz

# Replace these with your actual API keys
OPENCAGE_KEY = "999afd2052eb4bba8cecf0166703d614"
GEONAMES_USERNAME = "fajar_1096"

st.set_page_config(page_title="Prayer Times App", layout="centered")

st.markdown("<h1 style='text-align:center;'>🕌 Prayer Timings App</h1>", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def get_all_countries():
    url = "https://restcountries.com/v3.1/all?fields=name,cca2"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        data = res.json()
    except Exception as e:
        st.error(f"Failed to fetch countries data: {e}")
        return {}

    if not isinstance(data, list):
        st.error("Unexpected countries data format from REST Countries API.")
        return {}

    countries = {}
    for c in data:
        if not isinstance(c, dict):
            continue
        name = c.get("name", {}).get("common")
        cca2 = c.get("cca2")
        if name and cca2:
            countries[name] = cca2
    return dict(sorted(countries.items()))


@st.cache_data(show_spinner=False)
def get_cities_for_country(country_code):
    if not country_code:
        return []
    url = f"https://secure.geonames.org/searchJSON?country={country_code}&featureClass=P&maxRows=1000&username={GEONAMES_USERNAME}"
    try:
        res = requests.get(url, timeout=10).json()
        cities = set()
        for place in res.get("geonames", []):
            city_name = place.get("name")
            if city_name:
                cities.add(city_name)
        return sorted(cities)
    except Exception as e:
        st.error(f"Failed to fetch cities for {country_code}: {e}")
        return []


def validate_city_country(city, country):
    if not city or not country:
        return False
    try:
        geo = requests.get(
            f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={OPENCAGE_KEY}",
            timeout=10,
        ).json()
    except Exception as e:
        st.error(f"Location validation failed: {e}")
        return False

    if geo.get("total_results", 0) == 0:
        return False
    for r in geo.get("results", []):
        comp = r.get("components", {})
        if country.lower() in comp.get("country", "").lower():
            return True
    return False


countries = get_all_countries()
country = st.selectbox("Select Country", [""] + list(countries.keys()))

city = None
if country:
    country_code = countries.get(country)
    cities = get_cities_for_country(country_code)
    city = st.selectbox("Select City", [""] + cities)

if st.button("Get Prayer Timings"):
    if not country or not city:
        st.error("Please select both country and city.")
    else:
        if not validate_city_country(city, country):
            st.error("❌ Invalid combination — city does not match country.")
        else:
            try:
                url = f"https://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=2"
                data = requests.get(url, timeout=10).json()
                if data.get("code") != 200:
                    st.error("Unable to fetch prayer timings from API.")
                else:
                    timings = data["data"]["timings"]
                    tz = data["data"]["meta"]["timezone"]
                    greg = data["data"]["date"]["gregorian"]["date"]
                    hijri = data["data"]["date"]["hijri"]["date"]
                    local_time = datetime.now(pytz.timezone(tz)).strftime("%I:%M %p")
                    st.success(f"{city}, {country} — Local Time: {local_time} ({tz})")
                    st.write(f"📅 Gregorian: {greg} | 🗓 Hijri: {hijri} AH")
                    st.write("### 🕋 Prayer Times")
                    for name, tm in timings.items():
                        emoji = {
                            "Fajr": "🌅",
                            "Dhuhr": "🏙",
                            "Asr": "🌇",
                            "Maghrib": "🌆",
                            "Isha": "🌃",
                            "Sunrise": "☀️",
                        }.get(name, "🕌")
                        st.write(f"**{emoji} {name}:** {tm}")
            except Exception as e:
                st.error(f"Error fetching prayer timings: {e}")
