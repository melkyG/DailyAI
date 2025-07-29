import os

# Optionally: from openai import OpenAI (if you want to use OpenAI API)
# from openai import OpenAI
# import openai

# Format weather data into a prompt for the LLM

def format_weather_prompt(weather_data, location=None):
    daily = weather_data.get("daily", {})
    city = location.get("city") if location else None
    prompt = (
        f"The weather today"
        + (f" in {city}" if city else "")
        + f" is as follows: "
        f"High of {daily.get('maxtemp_c', '?')}°C, "
        f"low of {daily.get('mintemp_c', '?')}°C, "
        f"average humidity {daily.get('avghumidity', '?')}%, "
        f"max wind {daily.get('maxwind_kph', '?')} kph, "
        f"total precipitation {daily.get('totalprecip_mm', '?')} mm, "
        f"total snow {daily.get('totalsnow_cm', '?')} cm, "
        f"UV index {daily.get('uv', '?')}. "
        f"Condition: {daily.get('condition', '?')}. "
        f"Will it rain? {'Yes' if daily.get('daily_will_it_rain') else 'No'} "
        f"({daily.get('daily_chance_of_rain', '?')}% chance). "
        f"Will it snow? {'Yes' if daily.get('daily_will_it_snow') else 'No'} "
        f"({daily.get('daily_chance_of_snow', '?')}% chance). "
        "Based on this, what outfit should I wear?"
    )
    return prompt


import requests

def get_outfit_suggestion(weather_data, location=None):
    prompt = format_weather_prompt(weather_data, location)
    api_url = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    api_key = os.getenv("HF_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    payload = {"inputs": prompt}
    try:
        resp = requests.post(api_url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"].strip()
        if isinstance(data, dict) and "error" in data:
            return f"[LLM error: {data['error']}]"
        return f"[Unexpected LLM response: {data}]"
    except Exception as e:
        return f"[LLM API call failed: {e}]"

if __name__ == "__main__":
    # Example usage
    sample_weather = {
        "daily": {
            "maxtemp_c": 25,
            "mintemp_c": 15,
            "avgtemp_c": 20,
            "maxwind_kph": 18,
            "totalprecip_mm": 2,
            "totalsnow_cm": 0,
            "avghumidity": 60,
            "uv": 5,
            "condition": "Partly cloudy",
            "daily_will_it_rain": 1,
            "daily_chance_of_rain": 80,
            "daily_will_it_snow": 0,
            "daily_chance_of_snow": 0,
        }
    }
    print(get_outfit_suggestion(sample_weather, {"city": "New York"}))
