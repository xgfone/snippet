# -*- encoding: utf-8 -*-

import threading


class APIProxy(object):
    def __init__(self, load_api, *args, use_tpool=False, **kwargs):
        self._load_api = load_api
        self._use_tpool = use_tpool
        self._args = args
        self._kwargs = kwargs

        self._db_api = None
        self._lock = threading.Lock()

    @property
    def _api(self):
        if not self._db_api:
            with self._lock:
                if not self._db_api:
                    db_api = self._load_api(*self._args, **self._kwargs)
                    if self._use_tpool:
                        from eventlet import tpool
                        self._db_api = tpool.Proxy(db_api)
                    else:
                        self._db_api = db_api
        return self._db_api

    def __getattr__(self, name):
        return getattr(self._api, name)
