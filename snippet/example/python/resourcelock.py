from __future__ import unicode_literals, print_function, absolute_import, division

from threading import Lock
try:
    from queue import Queue
except ImportError:
    from Queue import Queue


class ResourceLock(object):
    def __init__(self):
        self._resources = {i: _ResourceLock() for i in range(0, 256)}

    def lock(self, id):
        if not id:
            raise ValueError("The argument cannot be empty")
        self._resources[ord(id[-1])].lock(id)

    def unlock(self, id):
        if not id:
            raise ValueError("The argument cannot be empty")
        self._resources[ord(id[-1])].unlock(id)


class _ResourceLock(object):
    def __init__(self):
        self._locker = Lock()
        self._waiters = {}
        self._resources = {}

    def lock(self, id):
        while not self._lock(id):
            pass

    def _lock(self, id):
        with self._locker:
            # Lock successfully.
            if id not in self._resources:
                self._resources[id] = None
                return True

            # Failed to lock, so wait that the other unlocks.
            if id not in self._waiters:
                self._waiters[id] = waiter = Queue()
            else:
                waiter = self._waiters[id]

            _lock = Lock()
            _lock.acquire()
            waiter.put(_lock)
        _lock.acquire()
        _lock.release()
        return False

    def unlock(self, id):
        with self._locker:
            if id not in self._resources:
                raise ValueError("The resource[%s] is not locked")

            self._resources.pop(id, None)
            waiter = self._waiters.get(id, None)
            if waiter is None:
                return

            try:
                _lock = waiter.get_nowait()
                _lock.release()
            except Exception:
                pass

            if waiter.empty():
                self._waiters.pop(id, None)


if __name__ == "__main__":
    from time import sleep
    from random import randint
    from threading import Thread

    rl = ResourceLock()
    id = "0123456789"

    def test(flag):
        sleep(randint(0, 3))
        print("++++++", flag)
        rl.lock(id)
        print(flag, "Lock")
        sleep(2)
        rl.unlock(id)
        print(flag, "Unlock")

    ts = []
    ts.append(Thread(target=test, args=("111",)))
    ts.append(Thread(target=test, args=("222",)))
    ts.append(Thread(target=test, args=("333",)))
    ts.append(Thread(target=test, args=("444",)))

    for t in ts:
        t.start()
    for t in ts:
        t.join()
    print("exit")
