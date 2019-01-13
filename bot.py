import logging
import os

from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram.utils.helpers import escape_markdown



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def help(bot, update):
    """Send a message when the command /help is issued."""
    logger.debug("Help received: %s", update.message.text)
    update.message.reply_text('Use the /wtf command!')


def start(bot, update):
    """Send a message when the command /start is issued."""
    logger.debug("Start received: %s", update.message.text)
    update.message.reply_text('Hi! Please use the WTF command to get data.')


def handle_wtf(bot, update):
    logger.debug("WTF received: %s", update.message.text)
    update.message.reply_text('Hello from the WTF command! There will be information here later.')


def handle_hello(bot, update):
    logger.debug("HELLO received: %s", update.message.text)
    update.message.reply_text("Servus, {}!".format(update.message.from_user.first_name))


def echo(bot, update):
    """Echo the user message."""
    logger.debug("Echo received: %s", update.message.text)
    update.message.reply_text(update.message.text)


def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query

    logger.debug("Inline query received: %s", query)
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]

    update.inline_query.answer(results)


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
    dp.add_handler(CommandHandler("hallo", handle_hello))
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
