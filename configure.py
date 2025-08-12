import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENCAGE_KEY = os.getenv("OPENCAGE_KEY")
GEONAMES_USERNAME = os.getenv("GEONAMES_USERNAME")

# API URLs
REST_COUNTRIES_URL = os.getenv("REST_COUNTRIES_URL")
ALADHAN_URL = os.getenv("ALADHAN_URL")

# Common headers for requests
HEADERS = {"User-Agent": "Mozilla/5.0"}
