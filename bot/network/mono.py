from ..config import dp
from ..lib.aioget import aioget


CURRENCIES = {
    840: "🇺🇸",
    980: "🇺🇦",
    978: "🇪🇺",
    643: "🇷🇺",
    985: "🇵🇱"
}


def get_emoji(code):
    emoji = CURRENCIES.get(code)
    return emoji if emoji is not None else code


@dp.message_handler(commands=["mono"])
async def monobank(message):
    res = await aioget("https://api.monobank.ua/bank/currency")

    msg = ""
    js = res.json()

    if isinstance(js, dict) and js["errorDescription"]:
        await message.reply(f"<code>{js['errorDescription']}</code>",
                            parse_mode="HTML")
        return
   
    for info in js[::2][:3]:
        msg += '{} ⇆ {}\n→ {} ₴\n← {} ₴\n\n'.format(
            get_emoji(info["currencyCodeA"]),
            get_emoji(info["currencyCodeB"]),
            info.get("rateBuy"),
            info.get("rateSell")
        )

    await message.reply(msg)
