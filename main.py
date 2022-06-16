import asyncio

import db


if __name__ == "__main__":
    asyncio.run(db.update_orders_in_database())
