import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler

from handlers import listDefinitionsHandler, definitionHandler, start, helloHandler, error, echo, inlinequery


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

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
    dp.add_handler(CommandHandler("wtf", definitionHandler.handle_command))
    dp.add_handler(CommandHandler("list", listDefinitionsHandler.handle_command))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("hallo", helloHandler.handle_command))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_handler(InlineQueryHandler(inlinequery))

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
