# 🕌 Prayer Timings App

A Streamlit-based app to fetch and display Islamic prayer timings for any city & country.

## Setup

1. Clone this repo.
2. Create a `.env` file with:
    ```
    OPENCAGE_KEY=your_opencage_key
    GEONAMES_USERNAME=your_geonames_username
    REST_COUNTRIES_URL=https://restcountries.com/v3.1/all?fields=name,cca2
    ALADHAN_URL=https://api.aladhan.com/v1/timingsByCity
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the app:
    ```bash
    streamlit run main.py
    ```

## Features
- Country & city selection
- City-country validation
- Real-time prayer timings
- Hijri & Gregorian date display
