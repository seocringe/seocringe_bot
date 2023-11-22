import asyncio
import pandas as pd


class WHOCCAtcDddIndex:

    def __init__(self):
        self.base_url = "https://www.whocc.no/atc_ddd_index"

    async def fetch_data(self):
        pass


async def scrape_and_save_atc_data():
    scraper = WHOCCAtcDddIndex()
    data = await scraper.fetch_data()

    df = pd.DataFrame(data)  # Пример: замените на фактическую обработку данных
    file_name = "atc_data.xlsx"
    df.to_excel(file_name, index=False)
    return file_name


# Эта часть для тестирования скрипта, если запускается как основная программа
if __name__ == "__main__":
    if not asyncio.get_event_loop().is_running():
        loop = asyncio.get_event_loop()
        file_path = loop.run_until_complete(scrape_and_save_atc_data())
        print(f"Data saved to {file_path}")
    else:
        print("Event loop is already running")