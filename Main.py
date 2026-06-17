import json
import sys
import urllib.parse
import urllib.request

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "weather-fetcher/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.load(resp)


def find_location(query):
    if not query:
        return None
    params = urllib.parse.urlencode({"name": query, "count": 1, "language": "en", "format": "json"})
    url = f"https://geocoding-api.open-meteo.com/v1/search?{params}"
    data = fetch_json(url)
    results = data.get("results")
    if not results:
        return None
    return results[0]


def fetch_weather(lat, lon):
    params = urllib.parse.urlencode({
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "timezone": "auto",
    })
    url = f"https://api.open-meteo.com/v1/forecast?{params}"
    return fetch_json(url)


def format_weather(location, weather):
    current = weather.get("current_weather", {})
    code = int(current.get("weathercode", 0))
    return (
        f"Location: {location.get('name')}, {location.get('country')}\n"
        f"Time: {current.get('time')}\n"
        f"Temperature: {current.get('temperature')}°C\n"
        f"Wind speed: {current.get('windspeed')} km/h\n"
        f"Condition: {WEATHER_CODES.get(code, 'Unknown')}"
    )


def main():
    if len(sys.argv) > 1 and sys.argv[1] in {"-h", "--help"}:
        print("Usage: python Main.py [city name]\nExample: python Main.py London")
        return 0

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter city name: ")
    location = find_location(query.strip())
    if not location:
        print("City not found. Try a different name.")
        return 1

    weather = fetch_weather(location["latitude"], location["longitude"])
    print(format_weather(location, weather))
    input("Press Enter to exit...")
    return 0
    input("Press Enter to exit...")


if __name__ == "__main__":
    raise SystemExit(main())

