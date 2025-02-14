""""
    This module contains unit tests for the 'weather.py' module, which handles
    weather data fetching and extraction functionality
"""
#pylint: disable=E0401
import unittest
from unittest.mock import patch, Mock
import requests
from weather import fetch_weather_forecast, format_weather_data

class TestFetchWeatherForecast(unittest.TestCase):
    """
    Testing the fetch_weather_forecast method
    """

    def setUp(self):
        """ Sample mock API response """
        #pylint: disable=C0301
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
        self.assertEqual(len(result), 1)
        self.assertEqual(result["day_1"][0]["name"], "Monday")
        self.assertEqual(result["day_1"][1]["name"], "Monday Night")

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
        #pylint: disable=C0301
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Internal Server Error")
        mock_get.return_value = mock_response

        result = fetch_weather_forecast()

        self.assertIsNone(result)

class TestFormatWeatherData(unittest.TestCase):
    """
    Testing the format_weather_data method
    """
    def test_basic_input(self):
        """
        Testing basic Input Functionality Using Diff Tests
        """
        sample_data = {
            "day_1": [
                {
                    "name": "Monday",
                    "temperature": 75,
                    "temperatureUnit": "F",
                    "probabilityOfPrecipitation": 20,
                    "windSpeed": "10 mph",
                    "windDirection": "S",
                    "detailedForecast": "Sunny with some clouds"
                },
                {
                    "name": "Monday Night",
                    "temperature": 55,
                    "temperatureUnit": "F",
                    "probabilityOfPrecipitation": 40,
                    "windSpeed": "5 mph",
                    "windDirection": "SW",
                    "detailedForecast": "Clear Skies"
                }
            ]
        }

        result = format_weather_data(sample_data)
        assert "Monday & Monday Night:" in result
        assert "Temperature: 75F" in result
        assert "Probability Of Precipitation: 40" in result
        assert "Wind Speed: 5 mph, Direction SW" in result
        assert "Detailed Forecast: Clear Skies" in result
