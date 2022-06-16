from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import config
import models
import cbrf
import google_sheets as gs


engine = None
google_service = None


async def update_orders_in_database():
    global engine, google_service

    if engine is None:
        engine = create_engine(
            f"postgresql+psycopg2://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}/{config.POSTGRES_DB}",
            echo=True,
            future=True,
        )
        models.Base.metadata.create_all(engine)

    if google_service is None:
        google_service = gs.auth()

    values = gs.get_values(google_service)
    rates = await cbrf.get_rates()

    costs_rub = list(map(round, [
        round(await cbrf.convert("USD", "RUB", float(u), rates))
        for u in values[gs.COST_USD_COL]
    ]))

    with Session(engine) as session:
        old_orders: list[models.Order] = session.query(models.Order).filter(models.Order.number.in_(values[gs.ORDER_NUMBER_COL])).all()
        for old_order in old_orders:
            old_order_index = values[gs.ORDER_NUMBER_COL].index(old_order.number)
            values[gs.ORDER_NUMBER_COL].pop(old_order_index)
            old_order.cost_rub = costs_rub.pop(old_order_index)
            old_order.cost_usd = values[gs.COST_USD_COL].pop(old_order_index)
            old_order.delivery_date = values[gs.DELIVERY_DATE_COL].pop(old_order_index)

        new_orders = []

        for number, cost_usd, cost_rub, delivery_date in zip(
            values[gs.ORDER_NUMBER_COL],
            values[gs.COST_USD_COL],
            costs_rub,
            values[gs.DELIVERY_DATE_COL],
        ):
            new_orders.append(
                models.Order(
                    number=number,
                    cost_usd=cost_usd,
                    cost_rub=cost_rub,
                    delivery_date=delivery_date,
                )
            )

        session.add_all(new_orders)
        session.commit()
