import os
import openai
from aiogram import types

from .. import handlers
from ..config import dp, GTRANSLATE_LANGS
from ..lib.text import cute_crop

# Ensure you've set the OPENAI_API_KEY as an environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def split_text(text, max_tokens=2048):
    words = text.split()
    parts = []
    current_part = []

    for word in words:
        if len(' '.join(current_part + [word])) > max_tokens:
            parts.append(' '.join(current_part))
            current_part = [word]
        else:
            current_part.append(word)
    parts.append(' '.join(current_part))
    
    return parts

async def translate_text(text: str, tgt_lang: str) -> str:
    text_parts = split_text(text)  # Split the text into parts
    translations = []  # List to hold the translated parts

    for part in text_parts:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты профессиональный переводчик."},
                {"role": "user", "content": f"Переведи на {tgt_lang} следующий текст: {part}"},
            ],
            max_tokens=2048,
            temperature=1,
        )
        translations.append(response['choices'][0]['message']['content'].strip())

    return ' '.join(translations)

@dp.message_handler(commands=[f"t{lang}" for lang in GTRANSLATE_LANGS])
@handlers.get_text
async def translate(message: types.Message, query: str):
    if (command := message.get_command().split("@")[0]) != "/tua":
        lang = command[2:]
    else:
        lang = "uk"

    text = await translate_text(query, tgt_lang=lang)

    await message.reply(cute_crop(text, limit=4096),
                        disable_web_page_preview=True)
