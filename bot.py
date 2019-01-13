import logging

from telegram.ext import Updater, CommandHandler
import os


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Use the /wtf command!')

def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Please use the WTF command to get data.')


def handle_wtf(bot, update):
    update.message.reply_text('Hello from the WTF command! There will be information here later.')

def main():
    logger.info("Starting up...")
    # Create the Updater and pass it your bot's token.
    token = os.environ["bot_token"]
    if token is None:
        logger.error("Cannot find bot_token env. variable that is required. Stopping.")
        exit(-1)

    updater = Updater(os.environ["bot_token"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("wtf", handle_wtf))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # log all errors
    dp.add_error_handler(error)

    logger.info("Configured. Start polling...")

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()