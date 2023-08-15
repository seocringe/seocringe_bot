##home/seocringe/seocringe_bot/bot/develop/netscape.py
from PIL import Image
import pytesseract, cachetools, requests
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State  # Добавьте этот импорт

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
    transformed_html = transform_html(requests.get(url).text)
    cache_dict[url] = transformed_html
    return transformed_html

request_limit = {}

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