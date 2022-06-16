from datetime import date

import httplib2
import googleapiclient.discovery
from googleapiclient.discovery import Resource
from oauth2client.service_account import ServiceAccountCredentials

import config


SHEET1 = "Лист1"
ORDER_NUMBER_COL = "заказ №"
COST_USD_COL = "стоимость,$"
DELIVERY_DATE_COL = "срок поставки"


def to_date(s: str) -> date:
    return date(*map(int, reversed(s.split("."))))


def auth() -> Resource:
    """authenticate to google api service"""

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        config.GOOGLE_CREDITS_PATH,
        [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    http_auth = credentials.authorize(httplib2.Http())
    return googleapiclient.discovery.build("sheets", "v4", http=http_auth)

def get_values(service: Resource) -> dict[str, list]:
    """
    get all values from table specified in SHEET1 variable

    Args:
    service - can be received from `auth` function

    Return:
    dict, keys - first row, values - all other rows in same collumn

    so table
      | A  | B    |
    1 | id | name |
    2 | 12 | john |
    3 | 15 | john |
    4 | 11 | john |

    turns into
    {
        "id": [12, 15, 11],
        "name": ["john", "john", "john"],
    }
    """

    result = service.spreadsheets().values().get(
        spreadsheetId=config.SPREADSHEET_ID,
        range=SHEET1,
        majorDimension="COLUMNS",
    ).execute()

    values = result["values"]
    result = {col[0]:col[1:] for col in values}
    result[ORDER_NUMBER_COL] = list(map(int, result[ORDER_NUMBER_COL]))
    result[COST_USD_COL] = list(map(int, result[COST_USD_COL]))
    result[DELIVERY_DATE_COL] = list(map(to_date, result[DELIVERY_DATE_COL]))
    return result
