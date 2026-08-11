import os

from dotenv import load_dotenv

load_dotenv()

API_KEY: str = os.environ.get("FOOTBALL_DATA_API_KEY")
BASE_URL: str = os.environ.get("FOOTBALL_API_BASE_URL")
HEADER_KEY: str = os.environ.get("HEADER_KEY")
