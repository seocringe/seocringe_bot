from distutils.core import setup  # Используйте нужный вам импорт
import re
import subprocess
from .config import settings
from ..agpt.agpt import GPT
from ..checkbacklinks.cbl import checkindex
import sys
sys.path.insert(0, '/workspaces/seocringe_bot')
import os
from aiogram import Bot, Dispatcher, types
from datetime import datetime
import lyricsgenius
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent

GENIUS_TOKEN = os.getenv('GENIUS_TOKEN')

def split_message_into_parts(text, max_part_len):
    paragraphs = text.split('\n')
    messages = []
    current_message = ""
    for paragraph in paragraphs:
        if len(paragraph) > max_part_len:
            words = paragraph.split(' ')
            current_paragraph = ""
            for word in words:
                if len(current_paragraph) + len(word) + 1 <= max_part_len:
                    current_paragraph += word + ' '
                else:
                    if len(current_message) + len(current_paragraph) <= max_part_len:
                        current_message += current_paragraph + '\n'
                    else:
                        messages.append(current_message)
                        current_message = current_paragraph + '\n'
                    current_paragraph = word + ' '
            if current_paragraph:
                if len(current_message) + len(current_paragraph) <= max_part_len:
                    current_message += current_paragraph + '\n'
                else:
                    messages.append(current_message)
                    current_message = current_paragraph + '\n'
        else:
            if len(current_message) + len(paragraph) + 1 <= max_part_len:
                current_message += paragraph + '\n'
            else:
                messages.append(current_message)
                current_message = paragraph + '\n'
    if current_message:
        messages.append(current_message)
    return messages


is_pytest_session = "pytest" in sys.modules
if is_pytest_session:
    class FakeUser:
        status: str = "fake"

        def is_chat_admin(self) -> bool:
            return True

    class FakeBot(Bot):
        async def get_chat_member(self, *args, **kwargs) -> FakeUser:
            return FakeUser()

    bot = FakeBot(token=settings.tokens.bot_token)
else:
    bot = Bot(token=settings.tokens.bot_token)

dp = Dispatcher(bot)
gpt_model = GPT(api_key='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')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет")


@dp.message_handler(commands=['gpt'])
async def respond_to_gpt_command(message: types.Message):
    user_input = message.text.replace('/gpt ', '')
    if message.reply_to_message:
        user_input = f"{message.reply_to_message.text}\n{user_input}"
    if user_input:
        response = gpt_model.get_reply(user_input)
        response_messages = split_message_into_parts(response, 4096)
        for response_message in response_messages:
            await message.reply(response_message.strip())
    else:
        await message.reply("Пожалуйста, введите текст после команды /gpt.")


@dp.message_handler(lambda message: message.reply_to_message and message.reply_to_message.from_user.id == bot.id)
async def respond_to_reply(message: types.Message):
    user_input = f"{message.reply_to_message.text}\n{message.text}"
    response = gpt_model.get_reply(user_input)
    response_messages = split_message_into_parts(response, 4096)
    for response_message in response_messages:
        await message.reply(response_message.strip())


@dp.message_handler(commands=['cbl'])
async def check_backlinks_command(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    backlinks = message.text.split('\n')[1:]
    results = []
    counter = 1
    for backlink in backlinks:
        parts = re.match(r"^(https?://[^\s]+)\s*(.*?)\s*(https?://[^\s]+)?$", backlink.strip())
        if parts:
            url, anchor, target_url = parts.groups()
            if not target_url and 'http' in anchor:
                target_url = anchor
                anchor = None
            result = checkindex(url, anchor, target_url)
            results.append(f"{counter}. {url if not target_url else target_url} {result}")
            counter += 1
        else:
            results.append(f"{counter}. Неверный формат обратной ссылки.")
            counter += 1
    current_time = datetime.now().strftime('%A %d.%m.%Y %H:%M')
    results.append(f"\n{current_time}")
    await message.reply('\n'.join(results))


@dp.message_handler(commands=['lyrics'])
async def lyrics_command(message: types.Message):
    song_name = message.text.replace('/lyrics ', '')
    if song_name:
        genius = lyricsgenius.Genius(GENIUS_TOKEN)
        song = genius.search_song(song_name)
        if song:
            await message.reply(song.lyrics)
        else:
            await message.reply("Sorry, I couldn't find that song.")
    else:
        await message.reply("Please enter the name of a song after the /lyrics command.")


if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, skip_updates=True)
