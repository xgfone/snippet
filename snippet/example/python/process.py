import time
import logging
import traceback

from multiprocessing import Process
from threading import Lock

LOG = logging.getLogger(__name__)


class _Task:
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.func(*self.args, **self.kwargs)


class ProcessManager:
    def __init__(self):
        self._tasks = {}
        self._lock = Lock()
        self._quit = False

    def _spawn_task(self, task):
        worker = Process(target=task)
        worker.daemon = True
        worker.start()
        return worker

    def launch_task(self, func, *args, **kwargs):
        workers = kwargs.pop("workers", 1)
        if workers < 1:
            raise ValueError("workers is less than 1")

        task = _Task(func, args, kwargs)
        worker = self._spawn_task(task)
        self._tasks[worker] = task

    def quit(self):
        with self._lock:
            self._quit = True

    def wait(self, reload=True):
        while True:
            time.sleep(1)

            with self._lock:
                if self._quit:
                    for worker in self._tasks:
                        worker.terminate()
                    return

            try:
                self._wait(reload)
            except Exception:
                LOG.error(traceback.format_exc())
                raise

    def _wait(self, reload):
        removes = []
        adds = []
        for worker, task in self._tasks.items():
            if not worker.is_alive():
                LOG.warning("Process[%d] exited", worker.pid)
                removes.append(worker)
                if reload:
                    worker = self._spawn_task(task)
                    adds.append((worker, task))

        for worker in removes:
            self._tasks.pop(worker)

        for worker, task in adds:
            self._tasks[worker] = task
            LOG.warning("Reload the task on Process[%d]: func=%s, args=%s, kwargs=%s",
                        worker.pid, task.func, task.args, task.kwargs)


if __name__ == "__main__":
    def test_task(interval=10):
        try:
            for i in range(1, 10):
                print(i, time.time())
                time.sleep(interval)
        except Exception as err:
            print(err)
        finally:
            print("Exit ...")

    m = ProcessManager()
    m.launch_task(test_task, interval=1)
    m.wait()
