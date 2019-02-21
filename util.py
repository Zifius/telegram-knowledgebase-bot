class _SingleInstance:

    def __init__(self, cls):
        self._target = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self._target(*args, **kwargs)
        return self._instance


def singleton(cls):
    return _SingleInstance(cls)
