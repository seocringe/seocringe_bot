import subprocess
import re
from urllib.parse import urlparse 
from aiogram import types
from ..config import dp

def split_text_into_parts(text, part_length = 4096):
    """This function splits the text into parts of length part_length"""
    return [text[i:i+part_length] for i in range(0, len(text), part_length)]

def extract_expiry_date(domain_text):
    """Extracts expiry date from a WHOIS response text"""
    for line in domain_text.split('\n'):
        if "expires:" in line.lower():
            expiry_date = line.split(":")[1].strip()
            return expiry_date
    return None

@dp.message_handler(commands=["whoisl"])
async def whoisList(message: types.Message):
    # Extract the domains from the message
    domains = message.text.split()[1:]

    domain_expiries = []
    for domain in domains:
        try:
            # Call whois command
            completed_process = subprocess.run(["whois", domain], capture_output=True, text=True)
            domain_text = completed_process.stdout

            # Extract expiry date
            expiry_date = extract_expiry_date(domain_text)
            if expiry_date is not None:
                domain_expiries.append((domain, expiry_date))
        except Exception as error:
            continue

    # Sort domains by expiry date
    domain_expiries.sort(key=lambda x: x[1])

    # Format output
    output = "\n".join(f"{d[0]}    {d[1]}" for d in domain_expiries)

    # Send output in parts, if needed
    for part in split_text_into_parts(output):
        await message.reply(text=part)
