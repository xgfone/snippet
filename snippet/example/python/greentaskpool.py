# -*- encoding: utf-8 -*-

import logging

LOG = logging.getLogger(__name__)


class GreenTaskPool(object):
    from threading import Thread

    def __init__(self, size=10000, use_eventlet=False, use_gevent=False,
                 auto_detection=False):
        self._size = size

        if use_eventlet:
            eventlet = __import__("eventlet")
            self._pool = self._init_eventlet(eventlet)
        elif use_gevent:
            gevent = __import__("gevent")
            self._pool = self._init_gevent(gevent)
        elif auto_detection:
            try:
                eventlet = __import__("eventlet")
                self._pool = self._init_eventlet(eventlet)
            except ImportError:
                try:
                    gevent = __import__("gevent")
                    self._init_gevent(gevent)
                except ImportError:
                    self._pool = None
                    LOG.warning("Use threading.Thread to execute the task.")
        else:
            self._pool = None
            LOG.warning("Use threading.Thread to execute the task.")

        self._spawn = self._pool.spawn if self._pool else GreenTaskPool._spawn_thread

    def _init_eventlet(self, eventlet):
        eventlet.monkey_patch(all=True)
        return eventlet.GreenPool(size=self._size)

    def _init_gevent(self, gevent):
        gevent.monkey.patch_all(httplib=True, sys=True)
        return gevent.pool.Pool(size=self._size)

    @staticmethod
    def _spawn_thread(func, *args, **kwargs):
        t = GreenTaskPool.Thread(target=func, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
        return t

    def spawn(self, func, *args, **kwargs):
        return self._spawn(func, *args, **kwargs)
