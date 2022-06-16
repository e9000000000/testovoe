import asyncio
from hashlib import sha1
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

_last_table_hash = ""


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


def get_values_raw(service: Resource) -> tuple[tuple[str]]:
    """get table values without formating"""

    return (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=config.SPREADSHEET_ID,
            range=SHEET1,
            majorDimension="COLUMNS",
        )
        .execute()["values"]
    )


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

    values = {col[0]: col[1:] for col in get_values_raw(service)}
    return {
        ORDER_NUMBER_COL: list(map(int, values[ORDER_NUMBER_COL])),
        COST_USD_COL: list(map(int, values[COST_USD_COL])),
        DELIVERY_DATE_COL: list(map(to_date, values[DELIVERY_DATE_COL])),
    }


async def wait_for_table_changes(service: Resource):
    """
    check every `config.TABLE_CHECK_COOLDOWN` for changes, if any - return, else - asyncio.sleep
    if runed first time after programm started: return without waiting

    Args:
    service - can be received from `auth` function
    """

    global _last_table_hash

    while 1:
        # cuz google didn't provide an easy way to set listener or i didn't find it. (websocket or something)
        new_table_hash = sha1(str(get_values_raw(service)).encode("utf-8")).hexdigest()
        if new_table_hash == _last_table_hash:
            await asyncio.sleep(config.TABLE_CHECK_COOLDOWN)
        else:
            _last_table_hash = new_table_hash
            return
