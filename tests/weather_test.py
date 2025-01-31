""""
    This module contains unit tests for the 'weather.py' module, which handles
    weather data fetching and extraction functionality
"""

import unittest
from unittest.mock import patch, Mock
import requests
from weather import fetch_weather_forecast

class TestFetchWeatherForecast(unittest.TestCase):
    """
    Testing the fetch_weather_forecast method
    """

    def setUp(self):
        """ Sample mock API response """
        self.mock_response = {
            "properties": {
                "periods": [
                    {"name": "Monday", "temperature": 70, "temperatureUnit": "F", "probabilityOfPrecipitation": {"value": 50}, "windSpeed": "10 mph", "windDirection": "N", "detailedForecast": "Sunny"},
                    {"name": "Monday Night", "temperature": 55, "temperatureUnit": "F", "probabilityOfPrecipitation": {"value": 20}, "windSpeed": "5 mph", "windDirection": "NW", "detailedForecast": "Clear"},
                    {"name": "Tuesday", "temperature": 75, "temperatureUnit": "F", "probabilityOfPrecipitation": {"value": 10}, "windSpeed": "8 mph", "windDirection": "NE", "detailedForecast": "Cloudy"},
                    {"name": "Tuesday Night", "temperature": 60, "temperatureUnit": "F", "probabilityOfPrecipitation": {"value": 30}, "windSpeed": "6 mph", "windDirection": "E", "detailedForecast": "Partly Cloudy"},
                    {"name": "Wednesday", "temperature": 80, "temperatureUnit": "F", "probabilityOfPrecipitation": {"value": 5}, "windSpeed": "12 mph", "windDirection": "S", "detailedForecast": "Hot"},
                    {"name": "Wednesday Night", "temperature": 65, "temperatureUnit": "F", "probabilityOfPrecipitation": {"value": 40}, "windSpeed": "7 mph", "windDirection": "SW", "detailedForecast": "Breezy"}
                ]
            }
        }
    
    @patch("requests.get")
    def test_successful_api_call(self, mock_get):
        """
        Test valid api response
        """
        mock_response = Mock()
        mock_response.json.return_value = self.mock_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = fetch_weather_forecast()

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
        self.assertEqual(result["day_1"][0]["name"], "Monday")
        self.assertEqual(result["day_3"][0]["name"], "Wednesday")

    @patch("requests.get")
    def test_api_connection_error(self, mock_get):
        """
        Test when the API is unreachable - Connection Error
        """
        mock_get.side_effect = requests.exceptions.ConnectionError

        result = fetch_weather_forecast()

        self.assertIsNone(result)
    
    @patch("requests.get")
    def test_api_404_error(self, mock_get):
        """
        Test when the API return a 404 Not Found

        (This should only ever happen if the API https url changes)
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        result = fetch_weather_forecast()

        self.assertIsNone(result)
    
    @patch("requests.get")
    def test_api_500_error(self, mock_get):
        """
        Test when the API return a 500 Server Error
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Internal Server Error")
        mock_get.return_value = mock_response

        result = fetch_weather_forecast()

        self.assertIsNone(result)