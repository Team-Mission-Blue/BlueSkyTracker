"""
BlueSky AI Weather Bot

This script fetches weather data from the National Weather Service (NWS) API,
processes it using the OpenAI API to generate natural language weather updates,
and posts these updates to BlueSky via its API.

Main Features:
- Fetches daily weather forecasts for specified locations.
- Formats the weather data into humand-readable updates.
- Automatically posts updates to BlueSky Daily,

Dependencies:

Author:
- Andrew Markarian
"""

import bluesky
import weather

def main():
    print("Loading Credentials...")
    bluesky_handle, bluesky_app_password = bluesky.load_bluesky_credentials()

    print("Athenticating...")
    access_token = bluesky.create_bluesky_session(bluesky_handle, bluesky_app_password)
    print("Authentication successful.")

    print("Fetching Forecast")
    forecast = weather.fetch_weather_forecast()
    print(forecast)
    
if __name__ == "__main__":
    main()