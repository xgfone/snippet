from __future__ import absolute_import, unicode_literals, print_function, division

import time

from queue import Queue, Empty
from threading import Lock


class _ResourcePoolSession(object):
    def __init__(self, pool, obj, close_on_exc=False):
        self.__pool = pool
        self.__obj = obj
        self.__close_on_exc = close_on_exc
        self.__closed = False

    def __repr__(self):
        return "ResourcePoolSession(obj={0})".format(self.__obj)

    def __getattr__(self, name):
        if self.__closed:
            raise RuntimeError("The session has been closed.")

        return getattr(self.__obj, name)

    def __del__(self):
        self.release_to_pool()

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, traceback):
        self.release_to_pool(ex_type is not None)

    def release_to_pool(self, close=False):
        """Release the obj into the resource pool.

        If close is True, close it at first, then create a new obj and put it
        into the resource pool.
        """

        if self.__closed:
            return
        self.__closed = True

        if close:
            try:
                self.__obj.close()
            except Exception:
                pass
            self.__obj = None

        self.__pool._put_from_session(self.__obj)

    def close(self):
        self.release_to_pool(close=True)


class ResourcePool(object):
    def __init__(self, cls, *args, capacity=0, idle_timeout=None, autowrap=False,
                 close_on_exc=False, **kwargs):
        """Create a new pool object.

        @param cls(object): The object class to be manage.
        @param args(tuple): The positional parameters of cls.
        @param kwargs(dict): The key parameters of cls.
        @param capacity(int): The maximum capacity of the pool.
                              If 0, the capacity is infinite.
        @param idle_timeout(int): The idle timeout. The unit is second.
                                  If None or 0, never time out.
        @param autowrap(bool): If True, it will wrap the obj in ResourcePoolSession
                               automatically, which will release the obj into the
                               pool when the session is closed or deleted.
        @param close_on_exc(bool): If True and autowrap is True, in with context,
                                   the session will close the obj firstly,
                                   then new an new one into the pool.
        """

        capacity = capacity if capacity >= 0 else 0

        self._cls = cls
        self._args = args
        self._kwargs = kwargs

        self._closed = False
        self._lock = Lock()
        self._capacity = capacity
        self._timeout = idle_timeout
        self._pools = Queue(capacity)
        self._autowrap = autowrap
        self._close_on_exc = close_on_exc

        while capacity > 0:
            self.put(None)
            capacity -= 1

    def __del__(self):
        self.close()

    def _get_now(self):
        return int(time.time())

    def _close_obj(self, obj):
        if obj:
            try:
                obj.close()
            except Exception:
                pass

    def close(self):
        """Close the pool and release all the objects.

        When closed, it will raise an RuntimeError if putting an object into it.
        """

        with self._lock:
            if self._closed:
                return
            self._closed = True

        while True:
            try:
                self._close_obj(self._pools.get_nowait()[0])
                self._pools.task_done()
            except Empty:
                return

    def get(self, timeout=None):
        """Get an object from the pool.

        When the pool is closed, it will raise a RuntimeError if calling this
        method.
        """

        with self._lock:
            if self._closed:
                raise RuntimeError("The pool has been closed.")

        _get = lambda obj: _ResourcePoolSession(self, obj, self._close_on_exc) \
            if obj and self._autowrap else obj

        if not self._capacity:
            try:
                obj = self._pools.get_nowait()
                self._pools.task_done()
            except Empty:
                obj = (self._cls(*self._args, **self._kwargs), self._get_now())
        else:
            obj = self._pools.get(timeout=timeout)
            self._pools.task_done()

        if obj and obj[0]:
            if self._timeout and self._get_now() - obj[1] > self._timeout:
                return _get(self.get(timeout=timeout))
            return _get(obj[0])

        return _get(self._cls(*self._args, **self._kwargs))

    def put(self, obj):
        """Put an object into the pool.

        When the pool is closed, it will close the object, not put it into the
        pool, if calling this method.
        """

        with self._lock:
            if self._closed:
                self._close_obj(obj)
                return

        if isinstance(obj, _ResourcePoolSession):
            obj.release_to_pool()
        else:
            self._pools.put_nowait((obj, self._get_now()))

    def put_with_close(self, obj):
        self._close_obj(obj)
        self.put(None)

    def _put_from_session(self, obj):
        self._pools.put_nowait((obj, self._get_now()))


def main(pool):
    o1 = pool.get()
    print(o1)

    o2 = pool.get()
    print(o2)

    def f():
        o3 = pool.get()
        print(o3)
        pool.put(o3)

    t = Thread(target=f)
    t.start()

    time.sleep(3)

    pool.put(o1)
    pool.put(o2)
    return t


if __name__ == "__main__":
    import time
    from threading import Thread

    class Obj(object):
        def __init__(self):
            self.time = time.time()
            time.sleep(0.1)

        def close(self):
            print("close {0}".format(self.time))

        def __repr__(self):
            return "Obj(time={0})".format(self.time)

    pool = ResourcePool(Obj, capacity=2, idle_timeout=1, autowrap=True)
    task = main(pool)
    time.sleep(1)
    task.join()
