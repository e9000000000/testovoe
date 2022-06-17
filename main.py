import asyncio

from db import Db
from tg import Bot
from google_sheets import GoogleApi


class Main:
    def __init__(self):
        self.g_api = GoogleApi()
        self.db = Db()
        self.bot = Bot(self.db)

    async def on_table_update(self):
        while 1:
            await self.g_api.wait_for_table_changes()
            values = self.g_api.get_values()
            await self.db.update_orders_in_database(values)
            await self.bot.send_notifications(values)

    def main(self):
        async def create_task(_):
            asyncio.create_task(self.on_table_update())
        self.bot.start_pooling(on_start=create_task)

if __name__ == "__main__":
    Main().main()
