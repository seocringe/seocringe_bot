import asyncio
import logging

from ..bot import bot

class ResendLogs(logging.Filter):
    def filter(self, record) -> bool:
        loop = asyncio.get_event_loop()
        loop.create_task(self.send_to_tg(record))
        return True

    async def send_to_tg(self, record):
        from ..bot import bot  # Move import here
        await bot.send_message(-1001435542296, record.msg, parse_mode="HTML")
