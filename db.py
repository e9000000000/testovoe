from copy import deepcopy

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_USER
from models import TgUser, Order, Base
from cbrf import get_rates, convert


class Db:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}",
            echo=True,
            future=True,
        )
        Base.metadata.create_all(self.engine)


    async def update_orders_in_database(self, values: list[dict]):
        """get data from table, add all orders to db, if order already in db (check by order number) - update it"""

        values = deepcopy(values)
        rates = await get_rates()
        for value in values:
            value["cost_rub"] = round(await convert("USD", "RUB", float(value["cost_usd"]), rates))

        with Session(self.engine) as session:
            new_numbers = list(map(lambda v: v["number"], values))
            existing_orders: list[Order] = (
                session.query(Order)
                .filter(Order.number.in_(new_numbers))
                .all()
            )
            for order in existing_orders:
                data_index = new_numbers.index(order.number)
                new_numbers.pop(data_index)
                old_order_data = values.pop(data_index)
                order.cost_rub = old_order_data["cost_rub"]
                order.cost_usd = old_order_data["cost_usd"]
                order.delivery_date = old_order_data["delivery_date"]

            new_orders = []

            for data in values:
                new_orders.append(
                    Order(
                        number=data["number"],
                        cost_usd=data["cost_usd"],
                        cost_rub=data["cost_rub"],
                        delivery_date=data["delivery_date"],
                    )
                )

            session.add_all(new_orders)
            session.commit()

    async def enable_notifications(self, tg_id: int):
        with Session(self.engine) as session:
            user = session.query(TgUser).filter(TgUser.tg_id==tg_id).one_or_none()
            if user is None:
                new_user = TgUser(tg_id=tg_id)
                session.add(new_user)
            else:
                user.notifiable = True
            session.commit()

    async def disable_notifications(self, tg_id: int):
        with Session(self.engine) as session:
            user = session.query(TgUser).filter(TgUser.tg_id==tg_id).one_or_none()
            if user is None:
                new_user = TgUser(tg_id=tg_id, notifiable=False)
                session.add(new_user)
            else:
                user.notifiable = False
            session.commit()

    async def get_notifiable_tg_users(self):
        with Session(self.engine) as session:
            return session.query(TgUser).filter(TgUser.notifiable==True).all()
