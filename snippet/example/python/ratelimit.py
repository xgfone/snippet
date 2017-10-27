import time

from threading import Thread
from queue import Queue


class RateLimiter:
    def __init__(self, limit, delay=0.01):
        num = int(limit * delay)
        if num < 1:
            raise ValueError("limit * delay < 1")

        self._limit_num = limit
        self._delay = delay
        self._num_per_delay = num
        self._queue = Queue(limit)

        self._thread = Thread(target=self._start)
        self._thread.daemon = True
        self._thread.start()

    def _start(self):
        total = int(self._limit_num * self._delay)
        while True:
            diff = total - self._queue.qsize()
            while diff > 0:
                self._queue.put(None)
                diff -= 1
            time.sleep(self._delay)

    def get_token(self):
        self._queue.get()
        self._queue.task_done()


if __name__ == "__main__":
    num = 100
    r = RateLimiter(10, 0.1)
    while num:
        r.get_token()
        print(num)
        num -= 1
