"""
This module handles all interactions with the Bluesky API, including authentication, 
session management, and posting formatted weather updates to the Bluesky social media platform.
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load enviornment variables from the .env file
def load_bluesky_credentials():
    """
    Validates and returns user BlueSky credentials
    """

    if load_dotenv():
        handle = os.getenv("BLUESKY_HANDLE")
        password = os.getenv("BLUESKY_APP_PASSWORD")
        assert handle != "", "BLUESKY_HANDLE can not be empty."
        assert password != "", "BLUE_APP_PASSWORD can not be empty."
        return (handle, password)
    print(".env does not exist.")
    sys.exit(1)

def create_bluesky_session(username: str, password: str):
    """
    Authenticate BlueSky credentials and create a session to recieve access token.

    returns:
    - Access token (accessJwt) for authentication.
    """
    url = "https://bsky.social/xrpc/com.atproto.server.createSession"
    payload = {"identifier": username, "password": password}

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        session = response.json()
        return session["accessJwt"]
    except requests.exceptions.RequestException as err:
        print("Error during authentication:", err)
        print("Response:", response.text if "response" in locals() else "No response")
        sys.exit(1)
