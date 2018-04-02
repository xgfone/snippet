# -*- encoding: utf-8 -*-

import time
import logging

from threading import Lock

LOG = logging.getLogger(__name__)


class LifeManager(object):

    def __init__(self):
        self._callbacks = []
        self._should_stop = False
        self._lock = Lock()
        self._stopped = False

    def register(self, func, *args, **kwargs):
        with self._lock:
            if self._stopped:
                raise RuntimeError("have stopped")
            self._callbacks.append((func, args, kwargs))

    def stop(self):
        with self._lock:
            if self._stopped:
                return
            self._stopped = True
            for func, args, kwargs in self._callbacks:
                try:
                    func(*args, **kwargs)
                except Exception as err:
                    LOG.error("Failed to execute %s: %s", func.__name__, err)
            self._should_stop = True

    def is_stopped(self):
        with self._lock:
            return self._stopped

    def run_forever(self):
        while True:
            with self._lock:
                if self._should_stop:
                    break
            time.sleep(1)

    def wait(self):
        if self.is_stopped():
            return
        self._wait()

    def _wait(self):
        lock = Lock()
        lock.acquire()
        self.register(lock.release)
        lock.acquire()
        lock.release()
