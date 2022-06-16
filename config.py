from os import getenv
from pathlib import Path


GOOGLE_CREDITS_PATH = Path("google_credits.json").resolve()
SPREADSHEET_ID = "1iuoIi09-b1UsyMXbYk0TSKRUguSJ7jgVG1q3VKrSy6g"

CBRF_RATES_URL = "https://www.cbr.ru/scripts/XML_daily.asp"

POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "")
POSTGRES_HOST = "localhost:5432"
POSTGRES_DB = "test"
