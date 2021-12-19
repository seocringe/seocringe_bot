from ..config import bot, Note, _

from .admin import check_admin
from .models import Article

from random import randint

from aiogram import types

from wikipya.clients import MediaWiki


def randomed_start(func):
    async def wrapper(message):
        if randint(0, 1) == 0:
            await func(message)

    return wrapper


def parse_arguments(limit, without_params=False):
    def argument_wrapper(func):
        async def wrapper(message):
            params = message.get_full_command()[1].split(maxsplit=limit - 1)

            if len(params) < limit and not without_params:
                await message.reply(
                    _("errors.few_args", num=limit), parse_mode="Markdown"
                )
            else:
                return await func(message, *params)

        return wrapper

    return argument_wrapper


def check(var, without_params=False):
    def argument_wrapper(func):
        async def wrapper(message):
            res = Note.get(message.chat.id, var)

            if res is None:
                res = "True"

            if str(res).title() == "True":
                await func(message)

        return wrapper

    return argument_wrapper


def get_text(func):
    @parse_arguments(1, without_params=True)
    async def wrapper(message, query=None):
        reply = message.reply_to_message

        if reply and reply.text:
            text = reply.text
        elif reply and reply.caption:
            text = reply.caption
        elif query:
            text = query
        else:
            await message.reply(_("errors.few_args", num=1), parse_mode="Markdown")
            return

        return await func(message, text)

    return wrapper


def only_jdan(func):
    async def wrapper(message):
        if message.from_user.id == 795449748:
            await func(message)

    return wrapper


def only_admins(func):
    async def wrapper(message):
        if message.chat.type == "supergroup" and await check_admin(message, bot):
            await func(message)

    return wrapper


def wikipya_handler(func):
    @send_article
    @parse_arguments(1, without_params=True)
    async def wrapper(message: types.Message, query: str) -> Article:
        wiki: MediaWiki = (await func(message)).get_instance()
        page, image, url = await wiki.get_all(query)

        return Article(page.parsed, None if image == -1 else image)

    return wrapper


def send_article(func):
    async def wrapper(message: types.Message, *args):
        result = await func(message, *args)

        if result.image:
            await message.answer_chat_action("upload_photo")
            await message.reply_photo(
                result.image,
                caption=result.text,
                parse_mode="HTML",
                reply_markup=result.keyboard,
            )
        else:
            await message.reply(
                result.text,
                parse_mode="HTML",
                disable_web_page_preview=True,
                reply_markup=result.keyboard,
            )

    return wrapper
