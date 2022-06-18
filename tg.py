import aiogram
import asyncio

from config import TGBOT_TOKEN
from db import Db
from models import Order


class Bot:
    response_template = "notifications: {status} /start - enable notifications\n/stop - disable notifications"
    notification_template = "{number} is outdated, delivery date is {date}"

    def __init__(self, db: Db):
        self.db = db
        self.bot = aiogram.Bot(TGBOT_TOKEN)
        self.dp = aiogram.Dispatcher(self.bot)

        @self.dp.message_handler(commands=["start"])
        async def start(message: aiogram.types.Message):
            await self.db.enable_notifications(message.from_user.id)
            await message.reply(Bot.response_template.format(status="ENABLED"))

        @self.dp.message_handler(commands=["stop"])
        async def stop(message: aiogram.types.Message):
            await self.db.disable_notifications(message.from_user.id)
            await message.reply(Bot.response_template.format(status="DISABLED"))

    async def send_notification(self, text: str):
        """send text message to all notifiable tg users"""

        users = await self.db.get_notifiable_tg_users()
        tasks = [
            asyncio.create_task(self.bot.send_message(u.tg_id, text)) for u in users
        ]
        for task in tasks:
            await task

    async def send_notifications(self):
        """send notifications about outdated orders. (only once for every date changing)"""

        outdated = await self.db.get_outdated_and_not_notified_orders()
        if len(outdated) <= 0:
            return

        texts = [
            Bot.notification_template.format(number=o.number, date=o.delivery_date)
            for o in outdated
        ]
        try:
            await self.send_notification("\n".join(texts))
            await self.db.mark_as_notified(outdated)
        except Exception as e:
            print(f"ERROR WHILE SENDING NOTIFICATION {type(e)}: {e}")

    def start_pooling(self, on_start=None):
        aiogram.executor.start_polling(self.dp, skip_updates=True, on_startup=on_start)
