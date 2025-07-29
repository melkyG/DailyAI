
from dotenv import load_dotenv
load_dotenv()
import requests
import os

# Query WeatherAPI.com with location (latitude, longitude)
def get_weather(latitude, longitude):
    """
    Returns weather data (temp, wind, precipitation, humidity, etc.) for the given coordinates.
    Uses WeatherAPI.com API.
    """
    api_key = os.getenv("WEATHERAPI_KEY")
import requests
import os

# Query WeatherAPI.com forecast endpoint with location (latitude, longitude)
def get_weather_forecast(latitude, longitude):
    """
    Returns daily and hourly weather data for the given coordinates using WeatherAPI.com forecast endpoint.
    Extracts data from forecastday -> day and forecastday -> hour.
    """
    api_key = os.getenv("WEATHERAPI_KEY")
    if not api_key:
        raise ValueError("WEATHERAPI_KEY not set in environment variables.")
    url = (
        f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={latitude},{longitude}&days=1&aqi=no&alerts=no"
    )
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        forecastday = data["forecast"]["forecastday"][0]
        day = forecastday["day"]
        # Extract daily summary
        daily = {
            "maxtemp_c": day["maxtemp_c"],
            "mintemp_c": day["mintemp_c"],
            "avgtemp_c": day["avgtemp_c"],
            "maxwind_kph": day["maxwind_kph"],
            "totalprecip_mm": day["totalprecip_mm"],
            "totalsnow_cm": day.get("totalsnow_cm", None),
            "avghumidity": day["avghumidity"],
            "uv": day.get("uv", None),
            "condition": day["condition"]["text"],
            "daily_will_it_rain": day.get("daily_will_it_rain", None),
            "daily_chance_of_rain": day.get("daily_chance_of_rain", None),
            "daily_will_it_snow": day.get("daily_will_it_snow", None),
            "daily_chance_of_snow": day.get("daily_chance_of_snow", None),
        }
        # Extract hourly data (list of dicts for each hour)
        hourly = []
        for hour in forecastday["hour"]:
            hourly.append({
                "time": hour["time"],
                "temp_c": hour["temp_c"],
                "condition": hour["condition"]["text"],
                "wind_kph": hour["wind_kph"],
                "humidity": hour["humidity"],
                "precip_mm": hour["precip_mm"],
            })
        return {"daily": daily, "hourly": hourly}
    except Exception as e:
        print(f"Error fetching weather forecast: {e}")
        return None

if __name__ == "__main__":
    # Example usage: test with sample coordinates (e.g., New York City)
    forecast = get_weather_forecast(40.7128, -74.0060)
    from pprint import pprint
    pprint(forecast)
        # ...existing code...
