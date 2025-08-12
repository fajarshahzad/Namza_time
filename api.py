import requests
import streamlit as st
from configure import HEADERS

def api_get(url, params=None, headers=None):
    """Generic GET request handler with error catching."""
    try:
        response = requests.get(url, params=params, headers=headers or HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None
