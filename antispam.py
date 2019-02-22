import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)


class AntiSpam:
    _lookup = {}

    def __init__(self, count=5, timeout=10) -> None:
        """
        Build an antispam checker that can check if an action was triggered a certain amount of times in the provided
         timeout
        :param count: of actions to be allowed within the configured time
        :param timeout: for which the actions are remembered and counted
        """
        self._count = count
        self._timeout = timeout

    def is_spam(self, identifier):
        """
        check if the current identifier has exceeded the amount of invocations in the given threshold
        :param identifier: string: unique identifier for the action to check against, e.g. user_id, user_id+operation
        :return: true if this is spam, false otherwise
        """
        logger.debug("Checking for spam for identifier: %s", identifier)
        AntiSpam._lookup.setdefault(identifier, []).append(time.time() + self._timeout)
        is_spam = len(self._lookup[identifier]) > self._count
        logger.debug("%s is spam: %s", identifier, is_spam)
        return is_spam

    @staticmethod
    def clean():
        """
        cleanup times that are pass the configured timeout
        :return: void
        """
        logger.debug("Cleaning up..")
        current_time = time.time()
        for identifier in AntiSpam._lookup:
            pruned = [t for t in AntiSpam._lookup[identifier] if t > current_time]
            if pruned:
                AntiSpam._lookup[identifier] = pruned
            else:
                AntiSpam._lookup.pop(identifier, None)


def spam_protect(count=5, timeout=10, message="You are too talkative, pls wait a bit and try again"):
    anti_spam = AntiSpam(count, timeout)

    def decorate(func):
        @wraps(func)
        def call(*args, **kwargs):
            if len(args) is 3:
                update = args[2]
                if anti_spam.is_spam(update.message.from_user.id):
                    update.message.reply_text(message)
                    return
            return func(*args, **kwargs)
        return call
    return decorate

