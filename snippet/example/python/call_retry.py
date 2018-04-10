# -*- encoding: utf-8

import time
import functools


class Retry(object):
    def __init__(self, max_retries=2, retry_interval=1, max_retry_interval=5,
                 increase_retry_interval=True):
        self._max_retries = max_retries
        self._retry_interval = retry_interval
        self._max_retry_interval = max_retry_interval
        self._increase_retry_interval = increase_retry_interval

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return self.call(func, *args, **kwargs)

        return wrapper

    def call(self, func, *args, **kwargs):
        interval = self._retry_interval
        remaining_retries = self._max_retries

        while True:
            try:
                return func(*args, **kwargs)
            except (IOError, OSError):
                if remaining_retries <= 0:
                    raise
                time.sleep(interval)
                if self._increase_retry_interval:
                    interval = min(interval * 2, self._max_retry_interval)
                remaining_retries -= 1
