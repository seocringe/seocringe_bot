from pytz import timezone

import logging
from datetime import datetime

from .config import DELAY, VK, RSS, IMAGE_PATH, RSS_FEEDS, VK_CHANNELS, STATUS
from .database import events, videos, warns, notes, conn
from .logger import logging
from .vk_api import vk_api
from .bot import bot, dp

START_TIME = datetime.now()
TIMEZONE = timezone("Europe/Moscow")
SCHEDULE = RSS or VK
