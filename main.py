"""Weather bot Python backend."""

import os
import pyowm
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext


load_dotenv()
owm_api = pyowm.OWM(os.environ['OWM_API_KEY'])
tg_bot = Bot(token=os.environ['TELEGRAM_BOT_TOKEN'])


def weather(update: Update, context: CallbackContext) -> None:
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
    None
    """
    location = context.args[0]  # get the location from the user
    try:
        observation = owm_api.weather_at_place(location)
        w = observation.get_weather()

        temperature = w.get_temperature('celsius')['temp']  # get temperature in Celsius
        status = w.get_detailed_status()  # get weather status

        message = f"The weather in {location} is {status} and the temperature is {temperature:.1f}°C"
    except pyowm.exceptions.api_response_error.NotFoundError:
        message = f"Sorry, I couldn't find any weather information for {location}"
    tg_bot.send_message(chat_id=update.effective_chat.id, text=message)


weather_handler = CommandHandler('weather', weather)
dispatcher = tg_bot.dispatcher
dispatcher.add_handler(weather_handler)
tg_bot.polling()
