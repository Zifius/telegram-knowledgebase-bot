import logging
import os

from telegram.ext import Updater, CommandHandler

from base import Base, engine
from handlers import start, error, help, DefinitionHandler, HelloHandler
from antispam import AntiSpam

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

    updater: Updater = Updater(os.environ["bot_token"])

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)

    definition_handler = DefinitionHandler()
    hello_handler = HelloHandler()


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("hallo", hello_handler.handle_hello))
    dp.add_handler(CommandHandler("wtf", definition_handler.handle_wtf))
    dp.add_handler(CommandHandler("list", definition_handler.handle_list))
    dp.add_handler(CommandHandler("def", definition_handler.handle_def))
    dp.add_handler(CommandHandler("rm", definition_handler.handle_rm))


    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # dp.add_handler(InlineQueryHandler(inlinequery))

    # TODO: use configuration here
    anti_spam = AntiSpam()

    # register anti spam cleanup with the bot's job queue
    updater.job_queue.run_repeating(callback=lambda *dont_care: anti_spam.clean(), interval=1, name="AntiSpam cleanup")

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
