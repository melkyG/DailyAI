
from location import get_location
from weather import get_weather_forecast
from llm import get_outfit_suggestion
from ui import show_outfit_suggestion
import streamlit as st
from streamlit_geolocation import streamlit_geolocation

# Orchestrate the flow: location → weather → LLM → output
def main():
    # 1. Try to get browser geolocation
    geo = streamlit_geolocation()
    if geo and geo.get('latitude') and geo.get('longitude'):
        latitude = geo['latitude']
        longitude = geo['longitude']
        location = {"latitude": latitude, "longitude": longitude, "city": None}
    else:
        # Fallback to IP-based location
        location = get_location()
        if not location:
            show_outfit_suggestion("Could not determine your location.")
            return
        latitude = location.get("latitude")
        longitude = location.get("longitude")
        if latitude is None or longitude is None:
            show_outfit_suggestion("Could not determine your coordinates.")
            return
    weather = get_weather_forecast(latitude, longitude)
    if not weather:
        show_outfit_suggestion("Could not fetch weather data.")
        return
    # 3. Get outfit suggestion from LLM
    suggestion = get_outfit_suggestion(weather, location)
    # 4. Show result in UI
    show_outfit_suggestion(suggestion)

if __name__ == "__main__":
    main()
