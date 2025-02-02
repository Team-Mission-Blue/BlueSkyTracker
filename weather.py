"""
This module handles all weather-related functionality within the project. It is responsible for 
fetching weather forecast data from the National Weather Service (NWS) API, parsing and extracting 
relevant information, and formatting it for use in other parts of the project.
"""
# pylint: disable=C0301
import requests

def fetch_weather_forecast():
    """
    Fetching Weather Data from NWS API

    We will be taking data specifically from Syracuse NY
    """
    try:
        url = "https://api.weather.gov/gridpoints/BGM/52,99/forecast"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        forecast = data.get("properties", {}).get("periods", [])

        forecast_days = []

        for i in range(4):
            period = forecast[i]
            forecast_days.append({
                "name": period.get("name"),
                "temperature": period.get("temperature"),
                "temperatureUnit": period.get("temperatureUnit"),
                "probabilityOfPrecipitation": period.get("probabilityOfPrecipitation", {}).get("value"),
                "windSpeed": period.get("windSpeed"),
                "windDirection": period.get("windDirection"),
                "detailedForecast": period.get("detailedForecast")
            })

        # Group forecast into two-day structure
        consolidated_forecast = {
            "day_1": forecast_days[:2],
            "day_2": forecast_days[2:4],
        }

        return consolidated_forecast

    except requests.exceptions.RequestException as err:
        print("Error Fetching Weather Data: ", {err})
        return None

def format_weather_data(weather_data):
    """
    This method is responsible for formatting the weather data retrieved from fetch_weather_data()
    """
    weather_input = ""
    for forecast in weather_data.values():
        weather_input += f"{forecast[0]['name']} & {forecast[1]['name']}:\n"
        for period in forecast:
            weather_input += (
                f"Temperature: {period['temperature']}{period['temperatureUnit']}\n"
                f"Probability Of Precipitation: {period['probabilityOfPrecipitation']}\n"
                f"Wind Speed: {period['windSpeed']}, Direction {period['windDirection']}\n"
                f"Detailed Forecast: {period['detailedForecast']}\n\n"
            )
    print(weather_input)
    return weather_input
