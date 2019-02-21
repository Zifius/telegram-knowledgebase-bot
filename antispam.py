import time
import logging
from util import singleton

logger = logging.getLogger(__name__)


@singleton
class AntiSpam:

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

    def is_spam(self, identifier):
        """
        check if the current identifier has not exceeded the amount of invocations in the given threshold
        :param identifier: string: unique identifier for the action to check against, e.g. user_id, user_id+operation
        :return: true if this is spam, false otherwise
        """
        logger.debug("Checking for spam for identifier: %s", identifier)
        self._lookup.setdefault(identifier, []).append(time.time())
        return len(self._lookup[identifier]) > self._count

    def clean(self):
        """
        cleanup times that are pass the configured timeout
        :return: void
        """
        logger.debug("Cleaning up..")
        threshold = time.time() - self._timeout
        for identifier in self._lookup:
            pruned = [t for t in self._lookup[identifier] if t > threshold]
            if pruned:
                self._lookup[identifier] = pruned
            else:
                self._lookup.pop(identifier, None)


def spam_protect(func):
    def call(*args, **kwargs):
        if len(args) is 3:
            update = args[2]
            if AntiSpam().is_spam(update.message.from_user.id):
                update.message.reply_text("You are too talkative, pls wait a bit and try again")
                return
        return func(*args, **kwargs)
    return call

