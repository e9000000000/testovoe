import httplib2
import googleapiclient.discovery
from googleapiclient.discovery import Resource
from oauth2client.service_account import ServiceAccountCredentials

import config


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
    get all values from 'Лист1' table

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
        range="Лист1",
        majorDimension="COLUMNS",
    ).execute()

    values = result["values"]
    return {col[0]:col[1:] for col in values}
