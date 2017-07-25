from datetime import datetime


class Timer:
    def __init__(self, started=False):
        self._elapsed = 0
        self._start = None if not started else datetime.now()

    def running(self):
        return self._start is not None

    def start(self):
        if self._start:
            raise Exception("Already started")
        self._start = datetime.now()

    def end(self):
        if not self._start:
            raise Exception("Not started")
        self._elapsed = (datetime.now() - self._start)
        self._start = None

    def elapsed(self):
        if self._start:
            return datetime.now() - self._start
        return self._elapsed

    def reset(self):
        if self._start:
            raise Exception("Running")
        self._start = None
        self._elapsed = 0

    def elapsed_str(self):
        return str(self)

    def elapsed_seconds(self):
        return self.elapsed().total_seconds()

    def __str__(self) -> str:
        delta = self.elapsed()
        s = delta.seconds
        ms = int(delta.microseconds / 1000)
        return '{:02}:{:02}:{:02}.{:03}'.format(s // 3600, s % 3600 // 60, s % 60, ms)
