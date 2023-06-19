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
from dotenv import load_dotenv
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from commands import start, cancel, weather, city_choice, button 
from commands import WEATHER, WEATHER_CHOICE


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.environ['TELEGRAM_BOT_TOKEN']).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WEATHER: [MessageHandler((filters.TEXT & ~filters.COMMAND) | filters.LOCATION, weather)],
            WEATHER_CHOICE: [CallbackQueryHandler(button)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel), 
            CommandHandler("get5", city_choice)
        ],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    load_dotenv()

    main()
