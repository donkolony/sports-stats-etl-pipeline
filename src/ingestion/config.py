import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

# Guard Clause: Raise error if api key is missing
if not API_KEY:
    raise ValueError("FOOTBALL_DATA_API_KEY is not set. Please check your .env file.")

BASE_URL = "https://api.football-data.org/v4/"
