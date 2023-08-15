##bot/config/__init__.py

from aiogram import Bot
from .config import settings
from .logger import logger

bot = Bot(token=settings.tokens.bot_token)

import pendulum as pdl

from pytz import timezone

from .config import (
    settings,
    LOCALES_DIR,
    WIKI_COMMANDS,
    WIKIPEDIA_SHORTCUTS
)

from .languages import LANGS, GTRANSLATE_LANGS, WIKIPEDIA_LANGS

from .logger import logger
from .bot import bot, dp
from .i18n import _


START_TIME = pdl.now()
TIMEZONE = timezone("Europe/Kiev")


__all__ = (
    settings,
    LANGS, GTRANSLATE_LANGS, WIKIPEDIA_LANGS,
    LOCALES_DIR, WIKI_COMMANDS, WIKIPEDIA_SHORTCUTS,
    logger,
    bot, dp,
    _
)
