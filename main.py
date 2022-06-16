import httplib2
import googleapiclient.discovery
from googleapiclient.discovery import Resource
from oauth2client.service_account import ServiceAccountCredentials

import config


def auth() -> Resource:
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
    result = service.spreadsheets().values().get(
        spreadsheetId=config.SPREADSHEET_ID,
        range="Лист1",
        majorDimension="COLUMNS",
    ).execute()

    values = result["values"]
    return {col[0]:col[1:] for col in values}
