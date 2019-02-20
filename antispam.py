import time
import logging

logger = logging.getLogger(__name__)


class AntiSpam:
    _count = None
    _timeout = None
    _lookup = {}

    def __init__(self, count=2, timeout=10) -> None:
        super().__init__()
        self._count = count
        self._timeout = timeout

    def is_spam(self, identifier):
        """
        check if the current identifier has exceeded the amount of invocations in the given threshold
        :param identifier: string: unique identifier for the action to check against, e.g. user_id, user_id+operation
        :return: true if this is not spam, false otherwise
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


anti_spam = AntiSpam()


def spam_protect(func):
    def call(*args, **kwargs):
        if len(args) is 3:
            update = args[2]
            if anti_spam.is_spam(update.message.from_user.id):
                update.message.reply_text("You are too talkative, pls wait a bit and try again")
                return
        return func(*args, **kwargs)
    return call

