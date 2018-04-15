# -*- coding: utf8 -*-

from time import time
from threading import Lock
from functools import wraps

STATE_CLOSED = "closed"
STATE_OPEN = "open"
STATE_HALF_OPEN = "half-open"


def get_now():
    return int(time())


class CircuitBreakerError(Exception):
    pass


class TooManyRequestsError(CircuitBreakerError):
    pass


class OpenStateError(CircuitBreakerError):
    pass


class Count(object):
    __slots__ = ("requests", "total_successes", "total_failures",
                 "consecutive_successes", "consecutive_failures")

    def __init__(self):
        self.requests = 0
        self.total_successes = 0
        self.total_failures = 0
        self.consecutive_successes = 0
        self.consecutive_failures = 0

    def on_request(self):
        self.requests += 1

    def on_success(self):
        self.total_successes += 1
        self.consecutive_successes += 1
        self.consecutive_failures = 0

    def on_failure(self):
        self.total_failures += 1
        self.consecutive_failures += 1
        self.consecutive_successes = 0

    def clear(self):
        self.requests = 0
        self.total_successes = 0
        self.total_failures = 0
        self.consecutive_successes = 0
        self.consecutive_failures = 0

    def copy(self):
        c = self.__class__.__new__()
        c.requests = self.requests
        c.total_successes = c.total_successes
        c.total_failures = c.total_failures
        c.consecutive_successes = c.consecutive_successes
        c.consecutive_failures = c.consecutive_failures
        return c


class CircuitBreaker(object):
    MAX_REQUESTS = 1
    COUNT_INTERVAL = 0
    RECOVERY_TIMEOUT = 60
    FAILURE_THRESHOLD = 5
    EXPECTED_EXCEPTION = Exception

    def __init__(self, name=None, max_requests=None, count_interval=None,
                 recovery_timeout=None, failure_threshold=None,
                 expected_exception=None, on_state_change=None):
        """The Circuit Breaker.
        """

        self._name = name
        self._max_requests = max_requests or self.MAX_REQUESTS
        self._count_interval = count_interval or self.COUNT_INTERVAL
        self._recovery_timeout = recovery_timeout or self.RECOVERY_TIMEOUT
        self._failure_threshold = failure_threshold or self.FAILURE_THRESHOLD
        self._expected_exception = expected_exception or self.EXPECTED_EXCEPTION
        self._on_state_change = on_state_change

        self._state = STATE_CLOSED
        self._generation = 0
        self._count = Count()
        self._expiry = 0
        self._lock = Lock()

        self._new_generation(get_now())

    @property
    def name(self):
        """Return the name of Circuit Breaker."""

        return self._name

    @property
    def state(self):
        """Return the state of Circuit Breaker."""

        with self._lock:
            return self._current_state(get_now())[0]

    @property
    def is_open(self):
        """Return True if the Circuit Breaker is open. Or False."""

        return self.state == STATE_OPEN

    @property
    def is_closed(self):
        """Return True if the Circuit Breaker is closed. Or False."""

        return self.state == STATE_CLOSED

    @property
    def is_half_open(self):
        """Return True if the Circuit Breaker is half-open. Or False."""

        return self.state == STATE_HALF_OPEN

    @property
    def count(self):
        """Return the count information of the requests."""

        with self._lock:
            return self._count.copy()

    def __call__(self, wrapped):
        """Decorate the function or method.

        Notice: when decorating more than one function or method, you should
        assign a unique name to the circuit breaker.
        """

        if not self._name:
            self._name = wrapped.__name__

        @wraps(wrapped)
        def wrapper(*args, **kwargs):
            return self.call(wrapped, *args, **kwargs)

        CircuitBreakerMonitor.register(self)
        return wrapper

    def allow(self):
        """Checks if a new request can proceed.

        It returns a callback that should be used to register the success
        or failure in a separate step.

        If the circuit breaker doesn't allow requests, it raises an exception.
        """

        generation = self._before_request()
        return lambda ok: self._after_request(generation, ok)

    def call(self, func, *args, **kwargs):
        """Run the given request if the CircuitBreaker accepts it.

        It raises an error if the CircuitBreaker rejects the request.
        Otherwise, it will return the result of the request.

        If an exception is raised in the request, the CircuitBreaker handles it
        as a failure and reraises it again.
        """

        generation = self._before_request()
        try:
            result = func(*args, **kwargs)
        except self._expected_exception:
            self._after_request(generation, False)
            raise
        else:
            self._after_request(generation, True)
            return result

    def _before_request(self):
        with self._lock:
            now = get_now()
            state, generation = self._current_state(now)
            if state == STATE_OPEN:
                raise OpenStateError
            elif state == STATE_HALF_OPEN and self._count.requests >= self._max_requests:
                raise TooManyRequestsError

            self._count.on_request()
            return generation

    def _after_request(self, before_generation, ok):
        with self._lock:
            now = get_now()
            state, generation = self._current_state(now)
            if generation != before_generation:
                return
            (self._on_success if ok else self._on_failure)(state, now)

    def _on_success(self, state, now):
        if state == STATE_CLOSED:
            self._count.on_success()
        elif state == STATE_HALF_OPEN:
            self._count.on_success()
            if self._count.consecutive_successes >= self._max_requests:
                self._set_statue(STATE_CLOSED, now)

    def _on_failure(self, state, now):
        if state == STATE_CLOSED:
            self._count.on_failure()
            if self._count.consecutive_failures > self._failure_threshold:
                self._set_statue(STATE_OPEN, now)
        elif state == STATE_HALF_OPEN:
            self._set_statue(STATE_OPEN, now)

    def _current_state(self, now):
        state = self._state
        if state == STATE_CLOSED:
            if self._expiry and self._expiry < now:
                self._new_generation(now)
        elif state == STATE_OPEN:
            if self._expiry < now:
                self._set_statue(STATE_HALF_OPEN, now)

        return self._state, self._generation

    def _set_statue(self, state, now):
        if self._state == state:
            return

        prev, self._state = self._state, state
        self._new_generation(now)
        if self._on_state_change:
            self._on_state_change(self._name, prev, state)

    def _new_generation(self, now):
        self._generation += 1
        self._count.clear()

        state = self._state
        if state == STATE_CLOSED:
            self._expiry = (now + self._count_interval) if self._count_interval else 0
        elif state == STATE_OPEN:
            self._expiry = now + self._recovery_timeout
        else:  # STATE_HALF_OPEN
            self._expiry = 0


class CircuitBreakerMonitor(object):
    circuit_breakers = {}

    @classmethod
    def register(cls, cb):
        """Register a circuit breaker."""

        cls.circuit_breakers[cb.name] = cb

    @classmethod
    def all_closed(cls):
        """Return True if all circuit breakers are closed."""

        return not cls.get_all_open()

    @classmethod
    def get_all_circuit_breakers(cls):
        """Return all circuit breakers."""

        return cls.circuit_breakers.values()

    @classmethod
    def get(cls, name):
        """Return the circuit breaker named 'name'."""

        return cls.circuit_breakers.get(name, None)

    @classmethod
    def get_all_open(cls):
        """Return all open circuit breakers."""

        return [cb for cb in cls.circuit_breakers.values() if cb.is_open]

    @classmethod
    def get_all_closed(cls):
        """Return all closed circuit breakers."""

        return [cb for cb in cls.circuit_breakers.values() if cb.is_closed]


def circuit_breaker(*args, cls=CircuitBreaker, **kwargs):
    """The decorator of CircuitBreaker.
    """

    if args and callable(args[0]):
        return cls()(args[0])
    return cls(*args, **kwargs)


if __name__ == "__main__":
    pass
