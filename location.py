import requests
import os

# Get user's location from IP using a public geolocation API

def get_location(ip=None):
    """
    Returns a dict with location info (city, region, country, lat, lon) for the given IP.
    If no IP is provided, uses the public IP of the caller.
    """
    api_url = os.getenv("IP_GEOLOCATION_API_URL", "https://ipapi.co/json/")
    if ip:
        url = f"{api_url}{ip}/json/"
    else:
        url = api_url
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country_name"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "ip": data.get("ip")
        }
    except Exception as e:
        print(f"Error fetching location: {e}")
        return None

if __name__ == "__main__":
    loc = get_location()
    print(loc)
