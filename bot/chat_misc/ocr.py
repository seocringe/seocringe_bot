import io
import cv2
import numpy as np
import pytesseract
from aiogram import types 
from aiogram.dispatcher import filters
from deep_translator import GoogleTranslator as DeepGoogleTranslator
from PIL import Image

from ..config import dp
from ..lib.text import cute_crop
from ..lib.errors import JdanbotError

def preprocess_image(image):
    return image

async def photo_to_string(photo: types.PhotoSize, lang: str) -> str | None:
    with io.BytesIO() as file:
        await photo.download(destination_file=file)
        file.seek(0)
        arr = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        preprocessed_image = preprocess_image(image)
        return pytesseract.image_to_string(Image.fromarray(preprocessed_image), lang=lang)

@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=[r"/(ocr_|o)([a-z]{2,3})(2|to)([a-z]{2})"]))
async def from_ocr(message: types.Message, regexp_command):
    ocr_lang, translate_to_lang = regexp_command.group(2), regexp_command.group(4)
    reply = message.reply_to_message
    languages = [
        lang for lang in pytesseract.get_languages() if lang.startswith(ocr_lang)
    ]
    if not languages:
        raise JdanbotError("errors.no_such_language")
    ocr_lang = languages[0]
    
    if reply.photo:
        if len(reply.photo) > 0:
            text = await photo_to_string(reply.photo[-1], ocr_lang)
        else:
            raise JdanbotError("errors.no_photo")
    else:
        raise JdanbotError("errors.no_photo")
    if text == "":
        raise JdanbotError("errors.failed_to_recognize")
    translate_to_lang = translate_to_lang if translate_to_lang != "ua" else "uk"
    t = DeepGoogleTranslator(
        source="auto",
        target=translate_to_lang,
    )
    text = t.translate(text)
    await message.reply(cute_crop(text, limit=4096), disable_web_page_preview=True)

@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=[r"/(ocr_|o)([a-z]{2,3})"]))
async def from_ocr_to_translated(message: types.Message, regexp_command):
    ocr_lang = regexp_command.group(2)
    reply = message.reply_to_message
    languages = [
        lang for lang in pytesseract.get_languages() if lang.startswith(ocr_lang)
    ]
    if not languages:
        raise JdanbotError("errors.no_such_language")
    ocr_lang = languages[0]
    
    if reply.photo:
        if len(reply.photo) > 0:
            text = await photo_to_string(reply.photo[-1], ocr_lang)
        else:
            raise JdanbotError("errors.no_photo")
    else:
        raise JdanbotError("errors.no_photo")
    if text == "":
        raise JdanbotError("errors.failed_to_recognize")
    await message.reply(text)
