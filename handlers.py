import logging
import random

# TODO add if inline mode is needed
# from uuid import uuid4
# from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode
# from telegram.utils.helpers import escape_markdown
from model import Definition, Channel, User, NotAuthorizedException
from base import transactional, Session
from mwt import MWT

logger = logging.getLogger(__name__)


class DefinitionHandler:

    @transactional
    def handle_list(self, bot, update):
        text = update.message.text
        logger.debug("/list received: %s", text)
        channel_telegram_id = update.message.chat.id

        definitions = Definition.find_all(channel_telegram_id)
        reply = update.message.reply_text

        if definitions:
            reply_list = "I know these definitions: \n"
            for definition in definitions:
                reply_list += "/wtf {}\n".format(definition.term)
        else:
            reply_list = "I don't have any definitions for current channel"

        reply(reply_list)

    @transactional
    def handle_wtf(self, bot, update):
        text = update.message.text
        logger.debug("/wtf received: %s", text)

        reply = update.message.reply_text
        parts = text.split(" ", 2)
        channel_telegram_id = update.message.chat.id

        if len(parts) <= 1:
            reply("Please provide a term for lookup.")
            return

        term = parts[1]
        definition = Definition.find_term(channel_telegram_id, term)

        if not definition:
            reply("I do not have any info for the term: '{}'".format(term))
        else:
            reply(("Term '{}' means: {}".format(definition.term, definition.content)))

    @transactional
    def handle_def(self, bot, update):
        text = update.message.text
        logger.debug("/def received: %s", text)
        channel_telegram_id = update.message.chat.id
        channel_telegram_name = update.message.chat.username

        user_telegram_id = update.message.from_user.id
        user_telegram_name = update.message.from_user.username

        reply = update.message.reply_text
        parts = text.split(" ", 2)
        if len(parts) == 3:
            term = parts[1]
            term_content = parts[2]
            try:
                user = User.find_create(user_telegram_id, user_telegram_name)
                channel = Channel.find_create(channel_telegram_id, channel_telegram_name)
                admins = get_admin_ids(bot, channel_telegram_id)
                if not admins:
                    # in case of private chats evey user is admin and has all rights
                    admins = [user_telegram_id]
                Definition.insert_update(user, channel, term, term_content, admins)
                logger.debug("Saved definition for %s", term)
                reply("Your definition for term '{}' has been saved".format(term))
            except NotAuthorizedException:
                reply("You are not authorised to change this definition '{}".format(term))
        else:
            reply("Please provide a term and it's content to create or update.")

    @transactional
    def handle_rm(self, bot, update):
        text = update.message.text
        logger.debug("/rm received: %s", text)
        channel_telegram_id = update.message.chat.id
        user_telegram_id = update.message.from_user.id

        reply = update.message.reply_text
        parts = text.split(" ", 2)

        if len(parts) <= 1:
            reply("Please provide a term to remove.")
            return

        term = parts[1]
        definition = Definition.find_term(channel_telegram_id, term)
        if definition is None:
            reply("Term '{}' I know not".format(term))
        else:
            # allowed only for channel admins and creator of definition
            admins = get_admin_ids(bot, channel_telegram_id) + [definition.user.telegram_id]
            if user_telegram_id in admins:
                Session().delete(definition)
                reply("Term '{}' was removed".format(definition.term))
            else:
                reply("You are not authorised to delete definition '{}'".format(term))


class HelloHandler:

    def __init__(self):
        self.greeting = [
            "Guten Tag", "Tag", "Hallo", "Grüß Gott", "Griaß Gott", "Grüß Dich", "Grüß Sie", "Griaß Eich", "Griaß Di",
            "Habe die Ehre", "Grüezi", "Grüessech", "Servus", "Heil", "Moin", "Abend", "Ahoi", "Willkommen", "Mahlzeit"
        ]

    def get_hello(self):
        hello_random = random.SystemRandom()
        return hello_random.choice(self.greeting)

    def handle_hello(self, bot, update):
        reply = update.message.reply_text

        reply(("{}, {}!".format(self.get_hello(), update.message.from_user.first_name)))


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def help(bot, update):
    """Send a message when the command /help is issued."""
    logger.debug("Help received: %s", update.message.text)
    update.message.reply_text('Use the /def, /wtf or /list command!')


def start(bot, update):
    """Send a message when the command /start is issued."""
    logger.debug("Start received: %s", update.message.text)
    update.message.reply_text('Hi! Please use /list to get all definitions and /wtf to get info for a term')


def echo(bot, update):
    """Echo the user message."""
    logger.debug("Echo received: %s", update.message.text)
    update.message.reply_text(update.message.text)


@MWT(timeout=60*60)
def get_admin_ids(bot, chat_id):
    """
    Returns a list of admin IDs for a given chat. Results are cached for 1 hour.
    Private chats and groups with all_members_are_administrator flag are handled as empty admin list
    """
    chat = bot.getChat(chat_id)
    if chat.type == "private" or chat.all_members_are_administrators:
        return []
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]

#
# def inlinequery(bot, update):
#     """Handle the inline query."""
#     query = update.inline_query.query
#
#     logger.debug("Inline query received: %s", query)
#     results = [
#         InlineQueryResultArticle(
#             id=uuid4(),
#             title="Caps",
#             input_message_content=InputTextMessageContent(
#                 query.upper())),
#         InlineQueryResultArticle(
#             id=uuid4(),
#             title="Bold",
#             input_message_content=InputTextMessageContent(
#                 "*{}*".format(escape_markdown(query)),
#                 parse_mode=ParseMode.MARKDOWN)),
#         InlineQueryResultArticle(
#             id=uuid4(),
#             title="Italic",
#             input_message_content=InputTextMessageContent(
#                 "_{}_".format(escape_markdown(query)),
#                 parse_mode=ParseMode.MARKDOWN))]
#
#     update.inline_query.answer(results)
