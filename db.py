from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_USER
from models import TgUser, Order, Base


class Db:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}",
            echo=True,
            future=True,
        )
        Base.metadata.create_all(self.engine)

    async def sync_orders_with_db(self, values: list[dict]):
        """get data from table, add all orders to db, if order already in db (check by order number) - update it"""

        new_orders = await Order.from_table_values(values)

        with Session(self.engine) as session:
            new_numbers = list(map(lambda v: v.number, new_orders))
            existing_orders: list[Order] = (
                session.query(Order).filter(Order.number.in_(new_numbers)).all()
            )
            for order in existing_orders:
                table_order_index = new_numbers.index(order.number)
                new_numbers.pop(table_order_index)
                new_order = new_orders.pop(table_order_index)
                order.cost_rub = new_order.cost_rub
                order.cost_usd = new_order.cost_usd
                order.set_delivery_date(new_order.delivery_date)

            session.add_all(new_orders)
            session.commit()

    async def enable_notifications(self, tg_id: int):
        """enable notificatins for tg user"""

        with Session(self.engine) as session:
            user = session.query(TgUser).filter(TgUser.tg_id == tg_id).one_or_none()
            if user is None:
                new_user = TgUser(tg_id=tg_id)
                session.add(new_user)
            else:
                user.notifiable = True
            session.commit()

    async def disable_notifications(self, tg_id: int):
        """disable notificatins for tg user"""

        with Session(self.engine) as session:
            user = session.query(TgUser).filter(TgUser.tg_id == tg_id).one_or_none()
            if user is None:
                new_user = TgUser(tg_id=tg_id, notifiable=False)
                session.add(new_user)
            else:
                user.notifiable = False
            session.commit()

    async def get_notifiable_tg_users(self) -> list[TgUser]:
        """get users with enabled notifications"""

        with Session(self.engine) as session:
            return session.query(TgUser).filter(TgUser.notifiable == True).all()

    async def get_outdated_and_not_notified_orders(self) -> list[Order]:
        """get outdated orders with outdated_notified=False"""

        with Session(self.engine) as session:
            now = datetime.now().date()
            return (
                session.query(Order)
                .filter(Order.outdated_notified == False, Order.delivery_date < now)
                .all()
            )

    async def mark_as_notified(self, orders: list[Order]):
        with Session(self.engine) as session:
            for order in orders:
                print(order)
                order.outdated_notified = True
                session.merge(order)  # TODO: send all in one sql request
            session.commit()
