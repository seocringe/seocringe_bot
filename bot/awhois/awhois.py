import subprocess
import re
from urllib.parse import urlparse 
from aiogram import types
from ..config import dp

def split_text_into_parts(text, part_length = 4096):
    """This function splits the text into parts of length part_length"""
    return [text[i:i+part_length] for i in range(0, len(text), part_length)]

def clean_and_format_text(text):
    """This function cleans and formats the text"""
    lines = text.split('\n')
    formatted_lines = []

    for i in range(len(lines)):
        if lines[i].startswith('%'):
            lines[i] = lines[i].upper()
            if 'REGISTRAR:' in lines[i]:
                formatted_lines.append('<b>REGISTRAR</b>')
            elif 'REGISTRANT:' in lines[i]:
                formatted_lines.append('<b>REGISTRANT</b>')
            elif 'ADMINISTRATIVE CONTACTS:' in lines[i]:
                formatted_lines.append('<b>ADMINISTRATIVE CONTACTS</b>')
            elif 'TECHNICAL CONTACTS:' in lines[i]:
                formatted_lines.append('<b>TECHNICAL CONTACTS</b>')
            elif 'QUERY TIME:' in lines[i]:
                formatted_lines.append('<b>QUERY TIME</b>')
        else:
            line = re.sub(r' +', ' ', lines[i].strip())
            if line != '':
                # check if the line contains a date
                if re.search(r'\b\d{4}-\d{2}-\d{2}\b', line) or line.lower().startswith(("created:", "modified:", "expires:")):
                    line = '<b>' + line.upper() + '</b>'  # if it does, convert the line to uppercase and bold
                formatted_lines.append(line)

    text = '\n'.join(formatted_lines)
    return text

@dp.message_handler(commands=["whois"])
async def whoisDomain(message: types.Message):
    # Extract the domain from the message, if it exists
    user_text = str(message.text).split()
    if len(user_text) < 2:
        await message.reply(
            text = "Пожалуйста, предоставьте доменное имя после /whois, например: /whois example.com",
            parse_mode="html"
        )
        return
    domain_name = user_text[1]
    try:
        # Call whois command
        completed_process = subprocess.run(["whois", domain_name], capture_output=True, text=True)
        domain_text = completed_process.stdout
        if domain_text == 'Socket not responding':
            await message.reply(
            text = f"""
            <b>TLD not supported\n</b>
            Please contact Admin\n
            """,
            parse_mode="html"
            )
        else:
            domain_text = clean_and_format_text(domain_text)
            user_text = split_text_into_parts(domain_text)
            for part in user_text:
                if part.strip():
                    await message.reply(
                        text = part,
                        parse_mode="html"
                    )
                else:
                    await message.reply(
                        text = "Информация WHOIS недоступна или пуста для данного домена.",
                        parse_mode="html"
                    )
    except Exception as error:
        await message.reply(
            text = f"""
            {error}\n 
            Please contact Admin\n 
            """,
            parse_mode="html"
        )
