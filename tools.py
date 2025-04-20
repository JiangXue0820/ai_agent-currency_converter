from modules import tool
import urllib.request
import urllib.parse
import json

@tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Converts currency using latest exchange rates.

    Parameters:
        - amount: The amount of money in old currency
        - from_currency: Source currency code (e.g., USD)
        - to_currency: Target currency code (e.g., EUR)  
    """
    try:
        url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())

        if 'rates' not in data:
            return "Error: Could not fetch exchange rates"
        
        rate = data['rates'].get(to_currency.upper())
        if not rate:
            return f"Error: Could not find exchange rate for {from_currency.upper()} -> {to_currency.upper()}"
        
        converted_amount = amount * rate
        
        return f"{amount} {from_currency.upper()} = {converted_amount:.2f} {to_currency.upper()}"
    
    except Exception as e:
        return f"Error converting currency: {str(e)}"


@tool()
def get_weather_by_city_and_date(city: str, date: str) -> str:
    """
    Fetches weather data (temperature and description) for a specific date and city.

    Parameters:
        - city: City name (e.g., "Tokyo")
        - date: Date in YYYY-MM-DD format (e.g., "2025-04-20")

    Returns:
        A string with weather info for the given date, including temperature and condition.
    """
    # Weather code to description mapping
    weather_descriptions = {
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
        99: "Thunderstorm with heavy hail"
    }

    try:
        # Step 1: Get latitude and longitude from city name
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1"

        with urllib.request.urlopen(geo_url) as geo_response:
            geo_data = json.loads(geo_response.read())

        results = geo_data.get("results")
        if not results:
            return f"Error: Could not find location for '{city}'."

        lat = results[0]["latitude"]
        lon = results[0]["longitude"]
        city_name = results[0]["name"]
        country = results[0].get("country", "")

        # Step 2: Fetch daily weather data
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&daily=temperature_2m_max,temperature_2m_min,weathercode"
            f"&start_date={date}&end_date={date}"
            f"&timezone=auto"
        )

        with urllib.request.urlopen(weather_url) as weather_response:
            weather_data = json.loads(weather_response.read())

        daily = weather_data.get("daily", {})
        if not daily or date not in daily["time"]:
            return f"No weather data found for {date} in {city_name}, {country}."

        i = daily["time"].index(date)
        temp_max = daily["temperature_2m_max"][i]
        temp_min = daily["temperature_2m_min"][i]
        code = daily["weathercode"][i]
        description = weather_descriptions.get(code, f"Unknown condition (code {code})")

        return (
            f"Weather in {city_name}, {country} on {date}:\n"
            f" - Max Temp: {temp_max}°C\n"
            f" - Min Temp: {temp_min}°C\n"
            f" - Condition: {description}"
        )

    except Exception as e:
        return f"Error fetching weather data: {str(e)}"
    
if __name__ == "__main__":
    convert_currency(100, 'USD', 'EUR')