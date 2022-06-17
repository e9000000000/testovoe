import asyncio
from hashlib import sha1
from datetime import date

import httplib2
import googleapiclient.discovery
from googleapiclient.discovery import Resource
from oauth2client.service_account import ServiceAccountCredentials

from config import SHEET_NAME, SPREADSHEET_ID, TABLE_CHECK_COOLDOWN, GOOGLE_CREDITS_PATH

def to_date(s: str) -> date:
    return date(*map(int, reversed(s.split("."))))

class GoogleApi:
    def __init__(self):
        self.last_table_hash = ""
        self.service = self.auth()


    def auth(self) -> Resource:
        """authenticate to google api service"""

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            GOOGLE_CREDITS_PATH,
            [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
        )
        http_auth = credentials.authorize(httplib2.Http())
        return googleapiclient.discovery.build("sheets", "v4", http=http_auth)


    def get_values_raw(self) -> tuple[tuple[str]]:
        """get table values without formating"""

        return (
            self.service.spreadsheets()
            .values()
            .get(
                spreadsheetId=SPREADSHEET_ID,
                range=SHEET_NAME,
                majorDimension="ROWS",
            )
            .execute()["values"]
        )


    def get_values(self) -> list[dict]:
        """
        get all values from table specified in SHEET1 variable

        Return:
        if table data is
          | A  | B     | C        | D             |
        1 | n  | order | cost_usd | delivery_date |
        2 | 1  | 12    | 111      | 15.12.2000    |
        3 | 2  | 15    | 218      | 17.2.2077     |

        return this
        [
            {
                "order": 12,
                "cost_usd": 111,
                "delivery_date": date(15.12.2000),
            },
            {
                "order": 15,
                "cost_usd": 218,
                "delivery_date": date(17.2.2077),
            },
        ]
        """

        return [{"number": int(row[1]), "cost_usd": int(row[2]), "delivery_date": to_date(row[3])} for row in self.get_values_raw()[1:]]


    async def wait_for_table_changes(self):
        """
        check every `config.TABLE_CHECK_COOLDOWN` for changes, if any - return, else - asyncio.sleep
        if runed first time after class created: return without waiting
        """

        while 1:
            # cuz google didn't provide an easy way to set listener or i didn't find it. (websocket or something)
            new_table_hash = sha1(str(self.get_values_raw()).encode("utf-8")).hexdigest()
            if new_table_hash == self.last_table_hash:
                await asyncio.sleep(TABLE_CHECK_COOLDOWN)
            else:
                self.last_table_hash = new_table_hash
                return
