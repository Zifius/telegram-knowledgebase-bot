from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool
from functools import wraps

Base = declarative_base()

# Create an engine that stores data in the local directory's
# bot.sqlite file.
engine = create_engine('sqlite:///bot.sqlite', poolclass=NullPool)

_SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(_SessionFactory)


# @MWT(timeout=60*60)
# TODO call clean up before switching on
def get_admin_ids(bot, chat_id):
    """
    Returns a list of admin IDs for a given chat. Results are cached for 1 hour.
    Private chats and groups with all_members_are_administrator flag are handled as empty admin list
    """
    chat = bot.getChat(chat_id)
    if chat.type == "private" or chat.all_members_are_administrators:
        return []
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]

def transactional(func):
    def call(*args, **kwargs):
        session = Session()
        try:
            result = func(*args, **kwargs)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return result
    return call


# TODO give creator rights
def only_admin(user_allowed=False):
    def decorate(func):
        @wraps(func)
        def call(*args, **kwargs):
            if len(args) is 3:
                bot = args[1]
                update = args[2]
                channel_telegram_id = update.message.chat.id
                user_telegram_id = update.message.from_user.id

                if not user_allowed:
                    admins = get_admin_ids(bot, channel_telegram_id)
                    if not admins:
                        # in case of private chats evey user is admin and has all rights
                        admins = [user_telegram_id]
                    if user_telegram_id not in admins:
                        update.message.reply_text("You are not authorised to perform this operation")
                        return
            return func(*args, **kwargs)
        return call
    return decorate
