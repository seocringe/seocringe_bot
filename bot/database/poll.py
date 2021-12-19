import datetime

from .connection import db
from ..config.bot import bot

from peewee import CharField, IntegerField, Model
from aiogram.utils import exceptions


class Poll(Model):
    user_id = IntegerField()
    chat_id = IntegerField()
    poll_id = IntegerField()
    timestamp = IntegerField()
    description = CharField()

    class Meta:
        db_table = "polls"
        database = db
        primary_key = False

    async def add(
        user_id: int,
        chat_id: int,
        poll_id: int,
        description: str
    ):
        now = datetime.datetime.now()
        period = int(now.timestamp())

        Poll.insert(chat_id=chat_id, user_id=user_id,
                    poll_id=poll_id, description=description,
                    timestamp=period).execute()

    async def close_old():
        period = datetime.timedelta(hours=24)
        now = datetime.datetime.now()
        period_bound = int((now - period).timestamp())

        polls = Poll.select() \
                    .where(Poll.timestamp <= period_bound).execute()

        for poll in polls:
            try:
                poll_res = await bot.stop_poll(poll.chat_id,
                                               poll.poll_id)

            except (exceptions.PollHasAlreadyBeenClosed,
                    exceptions.MessageWithPollNotFound):
                (Poll.delete()
                     .where(Poll.timestamp <= period_bound,
                            Poll.chat_id == poll.chat_id,
                            Poll.poll_id == poll.poll_id).execute())

                continue

            if poll_res.is_closed:
                Poll.delete() \
                    .where(Poll.timestamp <= period_bound).execute()

            else:
                await bot.stop_poll(poll.chat_id, poll.poll_id)
