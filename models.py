from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True)
    cost_usd = Column(Integer)
    cost_rub = Column(Integer)
    delivery_date = Column(Date)
