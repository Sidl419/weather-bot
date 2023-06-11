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
from utils import get_weather_status, format_wether_message

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
owm = OWM(os.environ['OWM_API_KEY'])
weather_mgr = owm.weather_manager()

WEATHER = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask the user about their gender."""
    await update.message.reply_text(
        "Hi! My name is Weather Bot. I will tell you the weather at your city. "
        "Send /cancel to stop talking to me.\n\n"
        "What is your location? Send me city name or geo location."
    )

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
        logger.info("Location of %s: %s", update.message.from_user, current_pos)
        observation = weather_mgr.weather_at_coords(*current_pos)
        weather_attrs = get_weather_status(observation)

        message = format_wether_message(weather_attrs)
    else:
        logger.info("Location of %s: %s", update.message.from_user, location)
        try:
            observation = weather_mgr.weather_at_place(location)  # the observation object is a box containing a weather object
            weather_attrs = get_weather_status(observation)

            message = format_wether_message(weather_attrs, location)

        except pyowm.commons.exceptions.NotFoundError:
            message = f"Sorry, I couldn't find any weather information for <b>{location}</b>"

    await update.message.reply_text(message, parse_mode=telegram.constants.ParseMode.HTML)

    return WEATHER


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel and end the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
