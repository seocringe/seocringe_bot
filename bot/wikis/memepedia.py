from aiogram import types

import re

import pymemeru

from ..config import dp, _
from .. import handlers
from ..lib.models import Article

from tghtml import TgHTML


@dp.message_handler(commands=["memepedia", "meme"])
@handlers.send_article
@handlers.parse_arguments(1)
async def mempep(message: types.Message, query: str) -> Article:
    try:
        search = await pymemeru.search(query)
    except AttributeError:
        await message.reply(_("errors.not_found"))
        return

    page = await pymemeru.page(search[0].name)
    text = TgHTML(str(page.cleared_text), [["img"]]).parsed

    print(page.title)

    return Article(
        text=text,
        image=page.main_image,
        href=f"https://memepedia.ru/{search[0].name}",
        title=page.title,
        force_format=True
    )
