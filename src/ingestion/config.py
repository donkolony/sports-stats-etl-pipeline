import os

from dotenv import load_dotenv

load_dotenv()

API_KEY: str = os.environ.get("FOOTBALL_DATA_API_KEY")
BASE_URL: str = os.environ.get("FOOTBALL_API_BASE_URL")
HEADER_KEY: str = os.environ.get("HEADER_KEY")

AVAILABLE_ENTITIES = ["matches", "teams", "standings"]

COMPETITION_MAP = {
    "CL": "UEFA Champions League",
    "BL1": "Bundesliga",
    "DED": "Eredivisie",
    "FL1": "Ligue 1",
    "EC": "European Championship",
    "SA": "Serie A",
    "PL": "Premier League",
}
