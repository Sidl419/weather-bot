"""
Weather bot Python backend.

First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
import pyowm
from pyowm.owm import OWM
from dotenv import load_dotenv
import logging
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

import telegram
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

load_dotenv()
owm = OWM(os.environ['OWM_API_KEY'])
weather_mgr = owm.weather_manager()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

WEATHER = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    await update.message.reply_text(
        "Hi! My name is Weather Bot. I will tell you the weather at your city. "
        "Send /cancel to stop talking to me.\n\n"
        "What is your location?"
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
    logger.info("Location of %s: %s", update.message.from_user, location)

    try:
        observation = weather_mgr.weather_at_place(location)  # the observation object is a box containing a weather object
        weather = observation.weather
        temp = weather.temperature('celsius').get('temp', None)  # get temperature in Celsius
        temp_feels = weather.temperature('celsius').get('feels_like', None)
        status = weather.detailed_status   # get weather status

        message = f"""The weather in {location} is <b>{status}</b>
The temperature is <b>{temp:.1f}°C</b>, feels like <b>{temp_feels:.1f}°C</b>"""
    except pyowm.commons.exceptions.NotFoundError:
        message = f"Sorry, I couldn't find any weather information for <b>{location}</b>"

    await update.message.reply_text(message, parse_mode=telegram.constants.ParseMode.HTML)

    return WEATHER


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.environ['TELEGRAM_BOT_TOKEN']).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WEATHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, weather)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
