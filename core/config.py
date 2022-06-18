from os import getenv
from pathlib import Path


GOOGLE_CREDITS_PATH = Path("google_credits.json").resolve()
SPREADSHEET_ID = "1iuoIi09-b1UsyMXbYk0TSKRUguSJ7jgVG1q3VKrSy6g"
TABLE_CHECK_COOLDOWN = 10  # seconds

SHEET_NAME = "Лист1"
SHEET_ORDER_NUMBER_COL = "заказ №"
SHEET_COST_USD_COL = "стоимость,$"
SHEET_DELIVERY_DATE_COL = "срок поставки"

CBRF_RATES_URL = "https://www.cbr.ru/scripts/XML_daily.asp"

POSTGRES_USER = getenv("POSTGRES_DB", "postgres")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "")
POSTGRES_HOST = "postgres:5432"
POSTGRES_DB = getenv("POSTGRES_DB", "test")

TGBOT_TOKEN = getenv("TGBOT_TOKEN", "")
