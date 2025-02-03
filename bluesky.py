"""
This module handles all interactions with the Bluesky API, including authentication, 
session management, and posting formatted weather updates to the Bluesky social media platform.
"""

import os
import sys
from dotenv import load_dotenv
from atproto import Client

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

def create_bluesky_post(username: str, password: str, post_text: str):
    """
    Creates post on BlueSky and returns its post link (URL)
    """
    client = Client()

    try:
        client.login(username, password)
    except Exception as e:
        raise RuntimeError(f"Login failed: {e}") from e

    try:
        post = client.send_post(post_text)
        post_id = post.uri.split('/')[-1]
    except Exception as e:
        raise RuntimeError(f"Post creation failed: {e}") from e

    url = f"https://bsky.app/profile/{username}/post/{post_id}"
    return url
