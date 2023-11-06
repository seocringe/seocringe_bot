# Импортируем библиотеку OpenAI, requests, datetime и os
from openai import OpenAI
import requests
from datetime import datetime
import os

# Получаем ключ API из переменной окружения
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Необходимо задать переменную окружения OPENAI_API_KEY")

# Создаем клиента OpenAI, используя ключ API
client = OpenAI(api_key=api_key)

try:
    # Генерируем изображение с помощью модели "dall-e-3"
    response = client.images.generate(
        model="dall-e-3",
        prompt="a white siamese cat",
        size="2048x2048",
        quality="high",
        n=1,
    )
except Exception as e:
    raise Exception("Ошибка при генерации изображения: ", e)

# Получаем URL сгенерированного изображения
image_url = response.data[0].url

try:
    # Загружаем изображение по полученному URL
    image_response = requests.get(image_url)
except Exception as e:
    raise Exception("Ошибка при загрузке изображения: ", e)

if image_response.status_code != 200:
    raise Exception("Не удалось загрузить изображение. Код статуса: ", image_response.status_code)

# Получаем текущую дату и форматируем ее в виде строки 'dd-mm-yyyy'
current_date = datetime.now().strftime("%d-%m-%Y")

# Формируем имя файла по шаблону 'dalle-[dd-mm-yyyy].png'
filename = f"dalle-{current_date}.png"

# Открываем файл на запись в двоичном формате
with open(filename, "wb") as f:
    # Записываем содержимое ответа в файл
    f.write(image_response.content)
