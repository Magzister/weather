import os

import telebot

from app.weather_service import VisualCrossing
from app.location_service import Geoapify
from app.sst_service import SeaTemperature
from app.db import DB
from app.formatter import format_weather
from app.types import Coordinates


bot = telebot.TeleBot(os.environ.get("TELEGRAM_BOT_TOKEN", ""))


@bot.message_handler(content_types=["location"])
def callback_message(message):
    lat, lon = message.location.latitude, message.location.longitude
    coords = Coordinates(latitude=lat, longitude=lon)
    weather = VisualCrossing().get_weather(coords)
    location = Geoapify().get_address(coords)
    # sst_href = DB().get_sst_hyperlink(location.country, location.city)
    # sst = SeaTemperature().get_sst(sst_href)
    sst = None
    bot.send_message(message.chat.id, format_weather(location, weather, sst))

bot.infinity_polling()
