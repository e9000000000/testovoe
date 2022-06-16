import asyncio

import db
import google_sheets as gs


async def handle_table_changes():
    table_service = gs.auth()
    while 1:
        await gs.wait_for_table_changes(table_service)
        await db.update_orders_in_database()


if __name__ == "__main__":
    asyncio.run(handle_table_changes())
