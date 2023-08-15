import requests
import xml.etree.ElementTree as ET
import csv
from urllib.parse import urlparse
import os
from datetime import datetime

MAX_MESSAGES = 10

async def extract_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    if response.status_code == 200:
        sitemap_content = response.content
        root = ET.fromstring(sitemap_content)
        urls = [element.text for element in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        return urls
    else:
        return []

async def extract_all_urls(sitemap_urls):
    urls = []
    for sitemap_url in sitemap_urls:
        if sitemap_url.endswith('.xml'):
            extracted_urls = await extract_urls_from_sitemap(sitemap_url)
            urls.extend(extracted_urls)
        else:
            urls.append(sitemap_url)
    return urls

async def generate_message_with_urls(chat_id, urls):
    if len(urls) > 0:
        message = f"Найдено {len(urls)} URL-адресов в сайтмапе:\n\n"
        for url in urls:
            message += f"- {url}\n"
        await bot.send_message(chat_id, message)
    else:
        await bot.send_message(chat_id, "Сайтмап не содержит URL-адресов.")

async def generate_files_with_urls(chat_id, urls):
    if len(urls) > MAX_MESSAGES:
        domain = urlparse(urls[0]).netloc
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        txt_filename = f"{domain}-sitemap-{timestamp}.txt"
        csv_filename = f"{domain}-sitemap-{timestamp}.csv"

        with open(txt_filename, 'w') as txt_file, open(csv_filename, 'w', newline='') as csv_file:
            txt_file.write('\n'.join(urls))
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["URL"])
            for url in urls:
                csv_writer.writerow([url])

        await bot.send_document(chat_id, document=types.InputFile(txt_filename), caption="Файл с URL-адресами (TXT)")
        await bot.send_document(chat_id, document=types.InputFile(csv_filename), caption="Файл с URL-адресами (CSV)")

        os.remove(txt_filename)
        os.remove(csv_filename)
    else:
        message = "Найдено URL-адресов в сайтмапе:\n\n"
        for url in urls:
            message += f"- {url}\n"
        await bot.send_message(chat_id, message)
