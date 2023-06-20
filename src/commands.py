"""Code for weather bot available commands."""

import telegram
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
import requests
import logging
import os
import pyowm
from pyowm.owm import OWM
from utils import get_weather_status, format_wether_message, build_menu, get_weather_msg_wrapper, get_weather_emodzi, _
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
    logging.info(_("You have no environment variable") + f"{e}")

WEATHER = 0
WEATHER_CHOICE = 1
WEATHER_CHOICE_WTTR = 2


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

    weather_emodzi_code = get_weather_emodzi(message.lower())
    await update.message.reply_text(weather_emodzi_code, parse_mode=telegram.constants.ParseMode.HTML)
    await update.message.reply_text(message, parse_mode=telegram.constants.ParseMode.HTML)

    return WEATHER


async def city_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Choose city from available list of buttons."""
    list_of_cities = [_('Moscow'), _('London'), _('Tokyo'), _('Paris'), _('Rome')]
    button_list = []
    for each in list_of_cities:
        button_list.append(types.InlineKeyboardButton(each, callback_data=each))
    reply_markup = types.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    bot.send_message(chat_id=update.message.chat_id,
                     text=_('Choose one city from the following or write yours'), reply_markup=reply_markup)

    return WEATHER_CHOICE


async def city_choice_wttr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Choose city from available list of buttons for forecast."""
    list_of_cities = [_('Moscow'), _('London'), _('Tokyo'), _('Paris'), _('Rome')]
    button_list = []
    for each in list_of_cities:
        button_list.append(types.InlineKeyboardButton(each, callback_data=each))
    reply_markup = types.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    bot.send_message(chat_id=update.message.chat_id,
                     text=_('Choose one city from the following'), reply_markup=reply_markup)

    return WEATHER_CHOICE_WTTR


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process the buttom push."""
    if update.callback_query is not None:
        location = update.callback_query.data
        msg = update.callback_query.message
        await msg.edit_text("\U0001f914")
        new_state = WEATHER

    elif update.message is not None:
        location = update.message.text
        msg = update.message
        new_state = WEATHER_CHOICE

    await msg.reply_text(_("You choose") + " <b>" + location + "</b>. " + _("Getting weather data..."),
                         parse_mode=telegram.constants.ParseMode.HTML)
    await msg.reply_text(get_weather_msg_wrapper(location, weather_mgr), parse_mode=telegram.constants.ParseMode.HTML)

    return new_state


async def button_wttr(update, context):
    """Process the buttom push for forecast."""
    if update.callback_query is not None:
        location = update.callback_query.data
        msg = update.callback_query.message
        await msg.edit_text("\U0001f914")
        new_state = WEATHER

    elif update.message is not None:
        location = update.message.text
        msg = update.message
        new_state = WEATHER_CHOICE_WTTR

    await msg.reply_text(_("You choose") + " <b>" + location + "</b>. " + _("Getting weather data..."),
                         parse_mode=telegram.constants.ParseMode.HTML)
    url = 'https://wttr.in/{}.png'.format(location)

    try:
        res = requests.get(url)
        await msg.reply_photo(res.content)
    except:
        message = _('Sorry, I could not find any weather information for') + f" <b>{location}</b>"
        await msg.reply_text(message, parse_mode=telegram.constants.ParseMode.HTML)

    return new_state


async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """List all available commands."""
    await update.message.reply_text(_("Welcome to weather-bot! You can use this commands:\n\
        -/start - for starting the conversation\n\
        -/get5 - to get weather from one of cities\n\
        -/getw - to get weather from one of cities for 3 days\n\
        -/help - for this help message\n\
        -/cancel - for ending conversation"))

    return WEATHER


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel and end the conversation."""
    user = update.message.from_user
    logger.info("%s %s %s.", _("User"), user.first_name, _("canceled the conversation"))
    await update.message.reply_text(
        _("Bye! I hope we can talk again some day."), reply_markup=ReplyKeyboardRemove()
    )
    await update.message.reply_text("\U0001f609", parse_mode=telegram.constants.ParseMode.HTML)

    return ConversationHandler.END
