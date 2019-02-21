import time
import logging
from functools import wraps
from weakref import WeakSet

logger = logging.getLogger(__name__)


class AntiSpam:
    __refs__ = WeakSet()

    def __init__(self, count=5, timeout=10) -> None:
        """
        Build an antispam checker that can check if an action was triggered a certain amount of times in the provided
         timeout
        :param count: of actions to be allowed within the configured time
        :param timeout: for which the actions are remembered and counted
        """
        self._lookup = {}
        self._count = count
        self._timeout = timeout
        AntiSpam.__refs__.add(self)

    def is_spam(self, identifier):
        """
        check if the current identifier has exceeded the amount of invocations in the given threshold
        :param identifier: string: unique identifier for the action to check against, e.g. user_id, user_id+operation
        :return: true if this is spam, false otherwise
        """
        logger.debug("Checking for spam for identifier: %s", identifier)
        self._lookup.setdefault(identifier, []).append(time.time())
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
        for instance in AntiSpam.__refs__:
            threshold = time.time() - instance._timeout
            for identifier in instance._lookup:
                pruned = [t for t in instance._lookup[identifier] if t > threshold]
                if pruned:
                    instance._lookup[identifier] = pruned
                else:
                    instance._lookup.pop(identifier, None)


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

