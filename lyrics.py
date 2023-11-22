import os
from lyricsgenius import Genius
from pyrogram import Client, filters, types
from requests.exceptions import Timeout, HTTPError
from pyrogram.errors import MessageTooLong
from config import Config

bot = Client(
    "bot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN
)
GENIUS = Genius(Config.TOKEN)


@bot.on_message(filters.command("start") & filters.private)
async def start(bot, message):
    await bot.send_message(
        message.chat.id,
        f"Hello **{message.from_user.first_name}**!!\n\nWelcome to Lyrics bot.",
        reply_markup=types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton(
                        "🔍Search inline...", switch_inline_query_current_chat="
                    "
                )
            ]
        ],
    )
)

@bot.on_message(filters.text & filters.private)
async def lyric_get(bot, message):
    try:
        m = await message.reply("🔍Searching...")
        song_name = message.text
        LYRICS = GENIUS.search_song(song_name)
        if LYRICS is None:
            await m.edit_text("❌Oops\nFound no result")
        TITLE, ARTISTE, TEXT = LYRICS.title, LYRICS.artist, LYRICS.lyrics
    except (Timeout, HTTPError) as e:
        print(e)
    try:
        await m.edit_text(
            f"🎶Song Name: **{TITLE}**\n🎙️Artiste: **{ARTISTE}**\n\n`{TEXT}`
           ", reply_markup=types.InlineKeyboardMarku
                p
                    (
                        [[types.InlineKeyboardButto
                            n("🔍Search for lyrics...", switch_inline_query_current_chat
                        =
                    "
                "
            ),
        ]]))
    except MessageTooLong:
        with open(f"downloads/{TITLE}.txt", "w") as file:
            file.write(f"{TITLE}\n{ARTISTE}\n\n{TEXT}")
            await m.edit_text(
                "Changed into a text file because the text is too long..."
            )
            await bot.send_document(
                message.chat.id,
                document=f"downloads/{TITLE}.txt",
                caption=f"\n{TITLE}\n{ARTISTE}",
            )
            os.remove(f"downloads/{TITLE}.txt")


@bot.on_inline_query()
async def inlinequery(client, inline_query):
    answer = []
    if inline_query.query == "":
        await inline_query.answer(
            results=[
                types.InlineQueryResultArticle(
                    title="Search to get lyrics...",
                    description="Lyrics bot",
                    reply_markup=types.InlineKeyboardMarkup(
                        [
                            [
                                types.InlineKeyboardButton(
                                    "🔍Search for Lyrics.."
                                   , switch_inline_query_current_chat=",
                                "
                            )
                        ]
                    ])
                   , input_message_content=types.InputTextMessageContent
                        ("Search for lyrics inline...
                    ",
                )
            )
        ])
    else:
        INLINE_SONG = inline_query.query
        INLINE_LYRICS = GENIUS.search_song(INLINE_SONG)
        INLINE_TITLE, INLINE_ARTISTE, INLINE_TEXT = (
            INLINE_LYRICS.title,
            INLINE_LYRICS.artist,
            INLINE_LYRICS.lyrics,
        )
        answer.append(
            types.InlineQueryResultArticle(
                title=INLINE_TITLE,
                description=INLINE_ARTISTE,
                reply_markup=types.InlineKeyboardMarkup(
                    [
                        [
                            types.InlineKeyboardButton(
                                "❌Wrong result?",
                                switch_inline_query_current_chat=INLINE_SONG,
                            ),
                            types.InlineKeyboardButton(
                                "🔍Search again..", switch_inline_query_current_chat="
                            ])
                        ]
                    ]
                ),
               , input_message_content=types.InputTextMessageContent
                    (f"**Inline lyrics result...**\n\n🎶Name: **{INLINE_TITLE}**\n🎙️Artiste: **{INLINE_ARTISTE}**\n\n`{INLINE_TEXT
                },
            `
        ")))
    await inline_query.answer(results=answer, cache_time=1)


bot.start()
