from sqlalchemy import Column, Integer, Date, BigInteger, Boolean
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True)
    cost_usd = Column(Integer)
    cost_rub = Column(Integer)
    delivery_date = Column(Date)


class TgUser(Base):
    __tablename__ = "tg_users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger)
    notifiable = Column(Boolean, default=True)
