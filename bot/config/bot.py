from distutils.core import setup
import re, subprocess, sys, os, datetime as dt, lyricsgenius
from .config import settings
from ..agpt.agpt import GPT
from ..checkbacklinks.cbl import checkindex
from aiogram import Bot, Dispatcher, types, executor

sys.path.insert(0, "/workspaces/seocringe_bot")
GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")

dp = Dispatcher(
    Bot(
        token=settings.tokens.bot_token
        if "pytest" not in sys.modules
        else FakeBot(token=settings.tokens.bot_token)
    )
)

gpt_model = GPT(api_key="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")


def split_message_into_parts(text, max_part_len):
    paragraphs, messages, current_message = text.split("\n"), [], ""
    for paragraph in paragraphs:
        if len(paragraph) > max_part_len:
            words, current_paragraph = paragraph.split(" "), ""
            for word in words:
                if len(current_paragraph) + len(word) + 1 <= max_part_len:
                    current_paragraph += word + " "
                else:
                    if len(current_message) + len(current_paragraph) <= max_part_len:
                        current_message += current_paragraph + "\n"
                    else:
                        messages.append(current_message)
                        current_message = current_paragraph + "\n"
                        current_paragraph = word + " "
            if current_paragraph:
                if len(current_message) + len(current_paragraph) <= max_part_len:
                    current_message += current_paragraph + "\n"
                else:
                    messages.append(current_message)
                    current_message = current_paragraph + "\n"
        else:
            if len(current_message) + len(paragraph) + 1 <= max_part_len:
                current_message += paragraph + "\n"
            else:
                messages.append(current_message)
                current_message = paragraph + "\n"
    if current_message:
        messages.append(current_message)
    return messages


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Привет")


@dp.message_handler(commands=["gpt"])
async def respond_to_gpt_command(message: types.Message):
    user_input = message.text.replace("/gpt ", "")
    if message.reply_to_message:
        user_input = f"{message.reply_to_message.text}\n{user_input}"
    if user_input:
        try:
            response = gpt_model.get_reply(user_input)
            response_messages = split_message_into_parts(response, 4096)
            for response_message in response_messages:
                await message.reply(response_message.strip())
        except Exception as e:
            await message.reply(f"Произошла ошибка: {e}")
    else:
        await message.reply("Пожалуйста, введите текст после команды /gpt.")


@dp.message_handler(
    lambda message: message.reply_to_message
    and message.reply_to_message.from_user.id == dp.bot.id
)
async def respond_to_reply(message: types.Message):
    user_input = f"{message.reply_to_message.text}\n{message.text}"
    response_messages = split_message_into_parts(gpt_model.get_reply(user_input), 4096)
    for response_message in response_messages:
        await message.reply(response_message.strip())


@dp.message_handler(commands=["cbl"])
async def check_backlinks_command(message: types.Message):
    await dp.bot.send_chat_action(message.chat.id, "typing")
    backlinks, results, counter = message.text.split("\n")[1:], [], 1
    for backlink in backlinks:
        parts = re.match(
            r"^(https?://[^\s]+)\s*(.*?)\s*(https?://[^\s]+)?$", backlink.strip()
        )
        if parts:
            url, anchor, target_url = parts.groups()
            if not target_url and "http" in anchor:
                target_url, anchor = anchor, None
            result = checkindex(url, anchor, target_url)
            results.append(
                f"{counter}. {url if not target_url else target_url} {result}"
            )
            counter += 1
        else:
            results.append(f"{counter}. Неверный формат обратной ссылки.")
            counter += 1
    results.append(f"\n{dt.datetime.now().strftime('%A %d.%m.%Y %H:%M')}")
    await message.reply("\n".join(results))


@dp.message_handler(commands=["lyrics"])
async def lyrics_command(message: types.Message):
    song_name = message.text.replace("/lyrics ", "")
    if song_name:
        song = lyricsgenius.Genius(GENIUS_TOKEN).search_song(song_name)
        if song:
            await message.reply(song.lyrics)
        else:
            await message.reply("Sorry, I couldn't find that song.")
    else:
        await message.reply(
            "Please enter the name of a song after the /lyrics command."
        )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)