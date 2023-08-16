##home/seocringe/seocringe_bot/bot/develop/netscape.py
from PIL import Image
import pytesseract, cachetools, requests
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State  # Добавьте этот импорт
from readability import Document
from bs4 import BeautifulSoup
from newspaper import Article
def extract_content_with_readability(html_content):
    doc = Document(html_content)
    content = doc.summary()
    title = doc.title()
    return title, content
def convert_html_to_telegram_format(html_content):
    return TgHTML(html_content).to_telegram()
def extract_image_content(image):
    return pytesseract.image_to_string(Image.open(image))

async def handle_photo(message, dp):
    file = await dp.bot.get_file(message.photo[-1].file_id)
    extracted_text = extract_image_content(await dp.bot.download_file(file.file_path))
    await dp.bot.send_message(chat_id=message.chat.id, text=extracted_text)

cache_dict = cachetools.TTLCache(maxsize=100, ttl=60 * 60)
def get_data_from_url(url):
    if url in cache_dict:
        return cache_dict[url]
    # NOTE: transform_html is not defined in the provided code
title, transformed_html = extract_content_with_readability(requests.get(url).text)
    telegram_content = convert_html_to_telegram_format(transformed_html)
    return title, telegram_content
request_limit = {}
title, content = get_data_from_url(url)
for message_part in split_long_messages(content):
    await dp.bot.send_message(chat_id=message.chat.id, text=message_part)

def is_url_allowed(user_id, url):
    if user_id not in request_limit:
        return True
    return False if url in request_limit[user_id] and request_limit[user_id][url] >= 5 else True

def update_request_limit(user_id, url):
    if user_id not in request_limit:
        request_limit[user_id] = {}
    limit = request_limit[user_id]
    limit[url] = limit[url] + 1 if url in limit else 1

# NOTE: response is not defined in the provided code
# if response.headers.get('Location'):
#     result = extract_and_transform(normalize_url(response.headers.get('Location')))

class Form(StatesGroup):
    Query = State()

async def send_menu(message, dp):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    keyboard_markup.add(
        types.InlineKeyboardButton('Поиск файла', callback_data='search_file'),
        types.InlineKeyboardButton('Настройки', callback_data='settings'),
        types.InlineKeyboardButton('Помощь', callback_data='help')
    )
    await dp.bot.send_message(chat_id=message.chat.id, text="Меню", reply_markup=keyboard_markup)
    def split_long_messages(text, max_length=4096):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]
