from aiogram import types
from ..config import dp


@dp.message_handler(commands=["donate"])
async def donate(message: types.Message):
    await message.reply("mono 5375 4114 2118 2424",
                        parse_mode="HTML",
                        disable_web_page_preview=True)
