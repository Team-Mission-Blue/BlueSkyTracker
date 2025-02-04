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
#pylint: disable=W0612

import bluesky
import weather
import ai

def main():
    """
    This runs the main module of BlueSkyTracker
    """
    print("Fetching Forecast...")
    forecast = weather.fetch_weather_forecast()

    print("Formatting Weather Data...")
    forecast = weather.format_weather_data(forecast)

    print("Generating AI Text...")
    post_text = ai.generate_ai_text(forecast)

    print("Loading BlueSky Credentials...")
    bluesky_handle, bluesky_app_password = bluesky.load_bluesky_credentials()

    print("Creating Post...")
    bluesky.create_bluesky_post(bluesky_handle, bluesky_app_password, post_text)

    print("Post Created Succesfully")

if __name__ == "__main__":
    main()
