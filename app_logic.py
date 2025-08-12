from datetime import datetime
import pytz
from data_fetcher import (
    get_all_countries,
    get_cities_for_country,
    validate_city_country,
    get_prayer_timings
)

def load_countries():
    """Load countries list for dropdown."""
    return get_all_countries()

def load_cities(country):
    """Load cities list for dropdown."""
    if not country:
        return []
    countries = get_all_countries()
    country_code = countries.get(country)
    return get_cities_for_country(country_code)

def fetch_prayer_data(city, country):
    """Fetch and prepare prayer data for UI display."""
    if not country or not city:
        return {"error": "Please select both country and city."}

    if not validate_city_country(city, country):
        return {"error": "❌ Invalid combination — city does not match country."}

    data = get_prayer_timings(city, country)
    if not data or data.get("code") != 200:
        return {"error": "Unable to fetch prayer timings from API."}

    timings = data["data"]["timings"]
    tz = data["data"]["meta"]["timezone"]
    greg = data["data"]["date"]["gregorian"]["date"]
    hijri = data["data"]["date"]["hijri"]["date"]
    local_time = datetime.now(pytz.timezone(tz)).strftime("%I:%M %p")

    emoji_map = {
        "Fajr": "🌅",
        "Dhuhr": "🏙",
        "Asr": "🌇",
        "Maghrib": "🌆",
        "Isha": "🌃",
        "Sunrise": "☀️"
    }

    return {
        "success": True,
        "city": city,
        "country": country,
        "local_time": local_time,
        "timezone": tz,
        "gregorian": greg,
        "hijri": hijri,
        "timings": {name: (emoji_map.get(name, "🕌"), time) for name, time in timings.items()}
    }
