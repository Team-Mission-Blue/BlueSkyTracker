import requests

def fetch_weather_forecast():
    """
    Fetching Weather Data from NWS API

    We will be taking data specifically from Syracuse NY
    """
    try:
        url = "https://api.weather.gov/gridpoints/BGM/52,99/forecast"

        response = requests.get(url)
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
    
def format_weather_data(weatherData):
    weather_input = ""
    for day, forecast in weatherData.items():
        weather_input += f"{forecast[0]["name"]} & {forecast[1]["name"]}:\n"
        for period in forecast:
            weather_input += (
                f"Temperature: {period["temperature"]}{period["temperatureUnit"]}\n"
                f"Probability Of Precipitation: {period["probabilityOfPrecipitation"]}\n"
                f"Wind Speed: {period["windSpeed"]}, Direction {period["windDirection"]}\n"
                f"Detailed Forecast: {period["detailedForecast"]}\n\n"
            )
    print(weather_input)
    return weather_input