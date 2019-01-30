import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.utils.helpers import escape_markdown
from model import userRepo, definitionRepo, User, Definition, Session

import hello

logger = logging.getLogger(__name__)


class PersistenceAwareHandler:

    def handle_command(self, bot, update):
        session = Session()
        try:
            self.handle(bot, update)
        finally:
            session.commit()
            Session.remove()

    def handle(self, bot, update):
        raise NotImplementedError("Not implemented")


class DefinitionHandler(PersistenceAwareHandler):

    def __init__(self, definition_repo):
        super().__init__()
        self.definitionRepo = definition_repo

    def handle_list(self, bot, update):
        definitions = self.definitionRepo.findAll()
        reply = update.message.reply_text
        for definition in definitions:
            reply("/wtf {}".format(definition))

    def handle(self, bot, update):
        text = update.message.text
        reply = update.message.reply_text
        logger.debug("WTF received: %s", text)
        parts = text.split(" ", 2)

        if len(parts) <= 1:
            reply("Please provide a term for lookup.")
            return

        term = parts[1]
        definition = self.definitionRepo.findByTerm(term)

        if len(parts) == 3:
            update_text = parts[2]
            if definition is None:
                definition = Definition(term=term, content=update_text)
            else:
                definition.content = update_text
            self.definitionRepo.persist(definition)
            logger.debug("saved definition for %s", term)
            reply("Your definition for term '{}' has been saved".format(term))
            return

        if definition is None:
            reply("I do not have any info for the term: '{}'".format(term))
        else:
            reply(("Term '{}' means: {}".format(definition.term, definition.content)))


class HelloHandler(PersistenceAwareHandler):

    def __init__(self, user_repo):
        super().__init__()
        self.userRepo = user_repo

    def handle(self, bot, update):
        user_id = update.message.from_user.id
        user_name = update.message.from_user.first_name
        reply = update.message.reply_text

        user = self.userRepo.findById(user_id)
        if user is None:
            logger.debug("Adding new user with ID {}".format(user_id))
            self.userRepo.persist(User(id=user_id, name=user_name))
        else:
            logger.debug("User {} exists".format(user_id))

        reply(("{}, {}!".format(hello.get_hello(), update.message.from_user.first_name)))


definitionHandler = DefinitionHandler(definitionRepo)
helloHandler = HelloHandler(userRepo)

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


