from datetime import datetime, date

from sqlalchemy import Column, Integer, Date, BigInteger, Boolean
from sqlalchemy.orm import declarative_base

from google_sheets import GoogleApi
from cbrf import get_rates, convert


Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True)
    cost_usd = Column(Integer)
    cost_rub = Column(Integer)
    delivery_date = Column(Date)
    outdated_notified = Column(Boolean, default=False)

    def __repr__(self):
        return f"Order({self.id=} {self.number=} {self.cost_usd=} {self.cost_rub=} {self.delivery_date=} {self.outdated_notified=})"

    @property
    def outdated(self):
        return self.delivery_date < datetime.now().date()

    @staticmethod
    async def from_table_values(values: list[dict]) -> list:
        rates = await get_rates()
        return [
            Order(
                number=v["number"],
                cost_usd=v["cost_usd"],
                cost_rub=round(
                    await convert("USD", "RUB", float(v["cost_usd"]), rates)
                ),
                delivery_date=v["delivery_date"],
            )
            for v in values
        ]

    def set_delivery_date(self, new_date: date):
        if self.delivery_date == new_date:
            return

        self.delivery_date = new_date
        self.outdated_notified = False


class TgUser(Base):
    __tablename__ = "tg_users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger)
    notifiable = Column(Boolean, default=True)

    def __repr__(self):
        return f"TgUser({self.id=} {self.tg_id=} {self.notifiable=})"
