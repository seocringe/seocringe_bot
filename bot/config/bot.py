# bot/config/bot.py

from aiogram import Bot, Dispatcher, types
from .config import settings
from ..agpt.agpt import GPT
from ..checkbacklinks.cbl import checkindex
import sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup
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



@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет")

@dp.message_handler(commands=['gpt'])
async def respond_to_gpt_command(message: types.Message):
    if message.reply_to_message:
        user_input = f"{message.reply_to_message.text}\n{message.text.replace('/gpt ', '')}"
    else:
        user_input = message.text.replace('/gpt ', '')
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

def format_whatweb_output(whatweb_output):
    lines = whatweb_output.split('\n')
    formatted_lines = []
    for line in lines:
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        line = ansi_escape.sub('', line)
        chunks = line.split('] ')
        url_status = chunks.pop(0) + ']'
        formatted_chunks = [url_status]
        for chunk in chunks:
            if '[' in chunk and ']' in chunk:
                key, value = chunk.split('[', 1)
                value = value.rstrip(' ,')
                formatted_chunks.append(f'{key.strip()} {value.strip()}')
        formatted_lines.append('\n'.join(formatted_chunks))
    return '\n\n'.join(formatted_lines)

async def send_txt_document(chat_id, text, filename):
    with open(filename, 'w') as f:
        f.write(text)
    await bot.send_document(chat_id, types.InputFile(filename))
    os.remove(filename)

@dp.message_handler(commands=['whatweb'])
async def whatweb_command(message: types.Message):
    urls = []
    if message.reply_to_message:
        urls.append(message.reply_to_message.text)
    if message.text:
        urls.extend(re.findall(r'(?:https?://)?[\w.-]+(?:\.[\w.-]+)+', message.text))
    if not urls:
        await message.reply("Пожалуйста, введите URL после команды /whatweb.")
        return
    results = []
    for url in urls:
        try:
            result = subprocess.run(['whatweb', url], stdout=subprocess.PIPE, text=True)
            formatted_output = format_whatweb_output(result.stdout)
            formatted_output = formatted_output.replace(', ', '\n')
            results.append(f"{url}\n{formatted_output}")
        except Exception as e:
            results.append(f"Ошибка при выполнении команды whatweb для {url}: {str(e)}")

    if len(results) > 0:
        document_text = '\n\n'.join(results)
        if len(document_text) <= 4096:
            await message.reply(document_text)
        else:
            filename = f"whatweb-{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            await send_txt_document(message.chat.id, document_text, filename)
@dp.message_handler(commands=['runscript'])
async def handle_run_script_command(message: types.Message):
    args = message.get_args().split(' ')
    if len(args) != 3:
        await message.reply("Please provide all three arguments.")
    else:
        # Здесь должна быть логика для функции run_script_command
        pass

@dp.message_handler(content_types=["photo"])
async def photo_handler(message):
    await handle_photo(message, dp)

@dp.message_handler(commands=['start'], state='*')
async def start_command(message):
    await send_menu(message, dp)

@dp.message_handler(commands=['netscape'])
async def netscape_command(message: types.Message):
    url = message.get_args()
    if not url:
        await message.reply("Пожалуйста, предоставьте URL после команды /netscape.")
        return

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Предположим, что статья находится в теге <article>
        article = soup.find('article')
        if not article:
            await message.reply("Не удалось найти статью на данной странице.")
            return

        # Отправляем содержимое статьи пользователю
        formatted_article = article.get_text(separator='\n').strip()
        await message.reply(formatted_article)

    except Exception as e:
        await message.reply(f"Произошла ошибка при обработке URL: {str(e)}")