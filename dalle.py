# Импортируем библиотеку OpenAI, requests и datetime
from openai import OpenAI
import requests
from datetime import datetime

# Создаем клиента OpenAI, используя ключ API
client = OpenAI(api_key="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")

# Генерируем изображение с помощью модели "dall-e-3"
# В качестве подсказки (prompt) используем "a white siamese cat"
# Размер изображения устанавливаем как "2048x2048"
# Качество изображения устанавливаем как "high"
# n=1 означает, что мы хотим сгенерировать только одно изображение
response = client.images.generate(
    model="dall-e-3",
    prompt="a white siamese cat",
    size="2048x2048",
    quality="high",
    n=1,
)

# Получаем URL сгенерированного изображения
image_url = response.data[0].url

# Загружаем изображение по полученному URL
image_response = requests.get(image_url)

# Получаем текущую дату и форматируем ее в виде строки 'dd-mm-yyyy'
current_date = datetime.now().strftime('%d-%m-%Y')

# Формируем имя файла по шаблону 'dalle-[dd-mm-yyyy].png'
filename = f"dalle-{current_date}.png"

# Открываем файл на запись в двоичном формате
with open(filename, "wb") as f:
    # Записываем содержимое ответа в файл
    f.write(image_response.content)