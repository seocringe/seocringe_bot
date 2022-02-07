import json
from datetime import datetime

import yaml
from aiogram import types

from ..config import dp, _
from ..lib import handlers
from ..lib.aioget import aioget
from ..lib.convert_bytes import convert_bytes
from ..lib.text import code
from ..lib.libtree import make_tree


@dp.message_handler(commands=["d"])
@handlers.only_jdan
@handlers.get_text
async def download(message: types.Message, query: str):
    response = await aioget(query)
    text = response.text

    try:
        text = yaml.dump(json.loads(text))
    except json.decoder.JSONDecodeError:
        pass

    await message.reply(code(text[:4096]),
                        parse_mode="HTML")


@dp.message_handler(commands=["wget", "r", "request"])
@handlers.only_jdan
@handlers.parse_arguments(1)
async def wget(message: types.Message, url: str):
    time = datetime.now()
    blacklist = ["mb", ".zip", ".7", ".gz", "98.145.185.175", ".avi",
                 "movie", "release", ".dll", "localhost", ".bin",
                 "0.0.0.1", "repack", "download"]

    if url.find("?") != -1:
        if url.split("/")[-1][:url.find("?")].find(".") != -1:
            await message.reply("Бан")
            return

    for word in blacklist:
        if url.lower().find(word) != -1:
            await message.reply(_("errors.url_in_blocklist"))
            return

    response = await aioget(url)

    load_time = datetime.now() - time
    main = str(load_time).split(":")

    tree = make_tree(dict(
        status=response.status_code,
        size=convert_bytes(len(response.content)),
        time=f"{main[1]}:{main[2][:main[2].find('.')]}"
    ), url)

    await message.reply(code(tree), parse_mode="HTML")
