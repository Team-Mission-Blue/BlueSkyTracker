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

        for i in range(6):
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
        
        # Group forecast into three-day structure
        consolidated_forecast = {
            "day_1": forecast_days[:2],
            "day_2": forecast_days[2:4],
            "day_3": forecast_days[4:6]
        }

        return consolidated_forecast
    
    except requests.exceptions.RequestException as err:
        print("Error Fetching Weather Data: ", {err})
        return None