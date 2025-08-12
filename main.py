import streamlit as st
from app_logic import load_countries, load_cities, fetch_prayer_data

st.set_page_config(page_title="Prayer Times App", layout="centered")
st.markdown("<h1 style='text-align:center;'>🕌 Prayer Timings App</h1>", unsafe_allow_html=True)

# Country selection
countries = load_countries()
country = st.selectbox("Select Country", [""] + list(countries.keys()))

# City selection
city = None
if country:
    cities = load_cities(country)
    city = st.selectbox("Select City", [""] + cities)

# Button action
if st.button("Get Prayer Timings"):
    result = fetch_prayer_data(city, country)

    if "error" in result:
        st.error(result["error"])
    else:
        st.success(f"{result['city']}, {result['country']} — Local Time: {result['local_time']} ({result['timezone']})")
        st.write(f"📅 Gregorian: {result['gregorian']} | 🗓 Hijri: {result['hijri']} AH")
        st.write("### 🕋 Prayer Times")
        for name, (emoji, tm) in result["timings"].items():
            st.write(f"**{emoji} {name}:** {tm}")
