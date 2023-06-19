"""Code for weather bot available commands."""

import telegram
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
import logging
import os
import pyowm
from pyowm.owm import OWM
from utils import get_weather_status, format_wether_message, build_menu, get_weather_msg_wrapper, _
import telebot
from telebot import types

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
try:
    owm = OWM(os.environ['OWM_API_KEY'])
    weather_mgr = owm.weather_manager()
    bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])
except KeyError as e:
    logging.info(f"You have no environment variable {e}")

WEATHER = 0
WEATHER_CHOICE = 1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask the user about their gender."""
    await update.message.reply_text(_("Hi! My name is Weather Bot. I will tell you the weather at your city. \n \
    Send /cancel to stop talking to me. \n What is your location? Send me city name or geo location."))

    return WEATHER


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Get current weather information for the specified location.

    Parameters
    ----------
    update : telegram.Update
        The update object representing the incoming message.
    context : telegram.ext.CallbackContext
        The context object for the bot handlers.

    Returns
    -------
    int
    """
    location = update.message.text  # get the location from the user
    if location is None:
        current_pos = (update.message.location.latitude, update.message.location.longitude)
        logger.info("%s %s: %s", _("Location of"), update.message.from_user, current_pos)
        observation = weather_mgr.weather_at_coords(*current_pos)
        weather_attrs = get_weather_status(observation)

        message = format_wether_message(weather_attrs)
    else:
        logger.info("%s %s: %s", _("Location of"), update.message.from_user, location)
        try:
            observation = weather_mgr.weather_at_place(location)  # the observation object is a box containing a weather object
            weather_attrs = get_weather_status(observation)

            message = format_wether_message(weather_attrs, location)

        except pyowm.commons.exceptions.NotFoundError:
            message = _('Sorry, I could not find any weather information for') + f" <b>{location}</b>"

    await update.message.reply_text(message, parse_mode=telegram.constants.ParseMode.HTML)

    return WEATHER

async def city_choice(update,context):
    list_of_cities = ['Moscow','London','Tokyo', 'Paris', 'Rome']
    button_list = []
    for each in list_of_cities:
        button_list.append(types.InlineKeyboardButton(each, callback_data = each))
    reply_markup=types.InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
    bot.send_message(chat_id=update.message.chat_id, text='Choose one city from the following',reply_markup=reply_markup)
    
    return WEATHER_CHOICE


async def button(update, context):   
    await update.callback_query.message.reply_text("You choose " + update.callback_query.data + ". Getting weather data...")
    await update.callback_query.message.reply_text(get_weather_msg_wrapper(update.callback_query.data, weather_mgr), parse_mode=telegram.constants.ParseMode.HTML)
    
    return WEATHER


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel and end the conversation."""
    user = update.message.from_user
    logger.info("%s %s %s.", _("User"), user.first_name, _("canceled the conversation"))
    await update.message.reply_text(
        _("Bye! I hope we can talk again some day."), reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
