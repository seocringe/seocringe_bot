import aiosqlite
from aiogram.utils import exceptions
from sqlfocus import SQLTableBase, SQLTable

import asyncio
# import json
import datetime

from .config import DB_PATH
from .bot import bot


import asyncio
import json

from peewee import *
from peewee_async import Manager

from .lib.async_sqlite import SqliteDatabase, onefor, get_count


db = SqliteDatabase(DB_PATH)


async def connect_db():
    return await aiosqlite.connect(DB_PATH)


class Videos(SQLTableBase):
    async def save(self, channelid, link):
        links = await self.select(where=f"{channelid = }")

        try:
            links = json.loads(links[0][1])[-15:]
            links.append(link)
        except IndexError:
            links = [link]

        links_str = json.dumps(links)

        await self.delete(where=f"{channelid = }")
        await self.insert(channelid, links_str)

        await self.conn.commit()


class Warn(Model):
    admin_id = IntegerField()
    user_id = IntegerField()
    chat_id = IntegerField()
    timestamp = IntegerField()
    reason = CharField()

    class Meta:
        db_table = "warns"
        database = db
        primary_key = False

    async def count_wtbans(user_id, chat_id,
                           period=datetime.timedelta(hours=24)):
        period_bound = int((datetime.datetime.now() - period).timestamp())

        return get_count(await manager.execute(
            Warn.select(fn.Count(SQL("*")))
                .where(
                    Warn.timestamp >= period_bound,
                    Warn.user_id == user_id,
                    Warn.chat_id == chat_id
                )
        ))

    async def mark_chat_member(user_id, chat_id, admin_id, reason):
        await manager.execute(
            Warn.insert(user_id=user_id, admin_id=admin_id,
                        chat_id=chat_id, reason=reason,
                        timestamp=int(datetime.datetime.now().timestamp()))
        )


class Pidors(SQLTableBase):
    async def getPidorInfo(self, chat_id,
                           period=datetime.timedelta(hours=24)):
        period_bound = int((datetime.datetime.now() - period).timestamp())
        return await self.select(where=[
            self.timestamp >= period_bound, f"{chat_id = }"
        ])


class Polls(SQLTableBase):
    async def add_poll(self, user_id, chat_id,
                       poll_id, description):
        now = datetime.datetime.now()
        period = int(now.timestamp())

        return await self.insert(chat_id, user_id, poll_id,
                                 description, period)


    async def close_old(self):
        period = datetime.timedelta(hours=24)
        now = datetime.datetime.now()
        period_bound = int((now - period).timestamp())

        where = self.timestamp <= period_bound
        polls = await self.select(where=where)

        for poll in polls:
            try:
                poll_res = await bot.stop_poll(poll[0], poll[2])

            except (exceptions.PollHasAlreadyBeenClosed,
                    exceptions.MessageWithPollNotFound):
                await self.delete(where=[
                    where,
                    f"chat_id = {poll[0]}",
                    f"poll_id = {poll[2]}"
                ])
                continue

            if poll_res.is_closed:
                await self.delete(where=where)
            else:
                await bot.stop_poll(poll[0], poll[2])


class Note(Model):
    chatid = IntegerField()
    content = CharField()
    name = CharField()

    class Meta:
        db_table = "notes"
        database = db
        primary_key = False

    async def add(chatid, name, text):
        await Note.remove(chatid, name)

        return await manager.execute(
            Note.insert(chatid=chatid, name=name, content=text)
        )

    async def get(chatid, name):
        note = onefor(await manager.execute(
            Note.select()
                .where(Note.chatid == chatid, Note.name == name)
        ))

        if note is not None:
            return note.content

    async def show(chatid):
        notes = await manager.execute(
            Note.select()
                .where(Note.chatid == chatid)
        )

        return [note.name for note in notes]

    async def remove(chatid, name):
        return await manager.execute(
            Note.delete()
                .where(Note.chatid == chatid, Note.name == name)
        )


class CommandStats(Model):
    chat_id = IntegerField()
    user_id = IntegerField()
    command = CharField()

    class Meta:
        db_table = "command_stats"
        database = db
        primary_key = False


class Event(Model):
    chatid = IntegerField()
    id = IntegerField()
    name = CharField()

    class Meta:
        db_table = "events"
        database = db
        primary_key = False

    async def reg_user_in_db(message):
        user = message.from_user

        cur_user = onefor(await manager.execute(
            Event.select()
                 .where(Event.id == user.id,
                        Event.chatid == message.chat.id)
        ))

        if cur_user is None:
            await manager.execute(
                Event.insert(
                    chatid=message.chat.id,
                    id=user.id,
                    name=user.full_name
                )
            )


conn = asyncio.run(connect_db())

videos = Videos(conn)
pidors = Pidors(conn)
polls = Polls(conn)

pidorstats = SQLTable("pidorstats", conn)


for model in (Note, Event, CommandStats, Warn):
    model.create_table(True)

manager = Manager(db)

db.close()
db.set_allow_sync(False)


async def init_db():
    await videos.create(exists=True, schema=(
        ("channelid", "TEXT"),
        ("links", "TEXT")
    ))

    await pidors.create(exists=True, schema=(
        ("chat_id", "INTEGER"),
        ("user_id", "INTEGER"),
        ("timestamp", "INTEGER")
    ))

    await pidorstats.create(exists=True, schema=(
        ("chat_id", "INTEGER"),
        ("user_id", "INTEGER"),
        ("username", "TEXT"),
        ("count", "INTEGER")
    ))

    await polls.create(exists=True, schema=(
        ("chat_id", "INTEGER"),
        ("user_id", "INTEGER"),
        ("poll_id", "INTEGER"),
        ("description", "TEXT"),
        ("timestamp", "INTEGER")
    ))

asyncio.run(init_db())
