# Configuration and environment variables

"""
Handles all configurations
Reads environmental variables and stores constants
"""

import os

from dotenv import load_dotenv

load_dotenv()

# Access the variables
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

# Guard Clause: Raise error if api key is missing
if not API_KEY:
    raise ValueError("FOOTBALL_DATA_API_KEY is not set. Please check your .env file.")

# URL
BASE_URL = "https://api.football-data.org/v4/"
