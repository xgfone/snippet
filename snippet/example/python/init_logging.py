import os
import sys
import time
import socket
import pickle
import struct
import logging

from logging.handlers import TimedRotatingFileHandler as _TimedRotatingFileHandler
from logging.handlers import DatagramHandler

LOG = logging.getLogger(__name__)
UNIX_DOMAIN_PATH = "/tmp/logging-unix-domain.sock"
DEFAULT_DATA_FMT = "%Y-%m-%d %H:%M:%S"
DEFAULT_FMT = "%(asctime)s - %(process)d - %(pathname)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s"


class TimedRotatingFileHandler(_TimedRotatingFileHandler):
    def __init__(self, filename, *args, **kwargs):
        if filename[-4:] == ".log":
            filename = "{0}.{1}{2}".format(filename[:-4], os.getpid(), filename[-4:])
        else:
            filename = "{0}.{1}".format(filename, os.getpid())
        super(TimedRotatingFileHandler, self).__init__(filename, *args, **kwargs)


def init_logging(logger=None, level="DEBUG", log_file="", init_handler=None,
                 max_count=30, propagate=False, file_config=None, dict_config=None,
                 unix_domain=None):
    fmt = DEFAULT_FMT
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    level = getattr(logging, level.upper())

    if log_file:
        if init_handler:
            handler = init_handler(log_file, max_count)
        else:
            handler = TimedRotatingFileHandler(log_file, when="midnight",
                                               interval=1, backupCount=max_count)
    elif unix_domain:
        handler = DatagramHandler(unix_domain, None)
    else:
        handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)

    # Initialize the argument logger with the arguments, level and log_file.
    root = logging.getLogger()
    if logger:
        loggers = logger if isinstance(logger, (list, tuple)) else [logger]
        for _logger in loggers:
            _logger.propagate = propagate
            _logger.setLevel(level)
            _logger.addHandler(handler)
            if root and root is _logger:
                root = None

    if root:
        root.propagate = propagate
        root.setLevel(level)
        root.addHandler(handler)

    # Initialize logging by the configuration file, file_config.
    if file_config:
        logging.config.fileConfig(file_config, disable_existing_loggers=False)

    # Initialize logging by the dict configuration, dict_config.
    if dict_config and hasattr(logging.config, "dictConfig"):
        logging.config.dictConfig(dict_config)


class LogFileWriter():
    """LogFileWriter writes the log into the file.

    Notice: the writer is not thread-safe.
    """
    def __init__(self, filename, size=100, backup_count=30, terminator="\n"):
        self.terminator = terminator
        self.max_bytes = size * 1024 * 1024
        self.backup_count = backup_count
        self.mode = "a"
        self.filename = os.path.abspath(filename)
        self.stream = None
        self._open()

    def __del__(self):
        self.close()

    def _open(self):
        self.stream = open(self.filename, self.mode)

    def _write(self, data):
        if self.stream is None:
            self._open()
        self.stream.write(data)
        self.stream.write(self.terminator)
        if hasattr(self.stream, "flush"):
            self.stream.flush()

    def should_rollover(self, data):
        if self.stream is None:
            self._open()

        if self.max_bytes > 0:
            self.stream.seek(0, 2)  # due to non-posix-compliant Windows feature
            if self.stream.tell() + len(data) >= self.max_bytes:
                return 1
        return 0

    def do_rollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        if self.backup_count > 0:
            for i in range(self.backup_count - 1, 0, -1):
                sfn = "%s.%d" % (self.filename, i)
                dfn = "%s.%d" % (self.filename, i + 1)
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.filename + ".1"
            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.filename, dfn)

        self.stream = self._open()

    def rotate(self, source, dest):
        if os.path.exists(source):
            os.rename(source, dest)

    def write(self, data):
        try:
            if self.should_rollover(data):
                self.do_rollover()
            self._write(data)
        except Exception as err:
            self.close()
            LOG.error(err)

    def close(self):
        if self.stream:
            self.stream.close()
            self.stream = None


def unix_domain_log_handler(unix_domain=None, logfile=None, size=100, count=100,
                            fmt=None, date_fmt=None):
    """The function is used in multiprocessing in general.

    For example,

        import logging
        from multiprocessing import Process
        from butils.init_logging import init_logging, unix_domain_log_handler

        LOG = logging.getLogger()
        UNIX_DOMAIN_PATH = "/tmp/unix-domain.sock"

        kwargs = {
            "unix_domain": UNIX_DOMAIN_PATH,
            "logfile": "/tmp/unix_domain.log",
            "size": 1,
        }
        t = Process(target=unix_domain_log_handler, kwargs=kwargs)
        t.daemon = True
        t.start()

        init_logging(unix_domain=UNIX_DOMAIN_PATH)
        LOG.info("test log write")
    """
    fmt = fmt if fmt else DEFAULT_FMT
    date_fmt = date_fmt if date_fmt else DEFAULT_DATA_FMT
    if logfile:
        file = LogFileWriter(logfile, size, count)
    else:
        file = sys.stderr

    unix_domain = unix_domain if unix_domain else UNIX_DOMAIN_PATH
    if os.path.exists(unix_domain):
        os.unlink(unix_domain)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.bind(unix_domain)
    while True:
        try:
            datas = sock.recvfrom(65535)
            data = datas[0]
            if len(data) < 4:
                continue
            _len = struct.unpack(">L", data[:4])[0]
            data = data[4:]
            if len(data) != _len:
                LOG.warning("The data length is not right")
                continue
            data = pickle.loads(data, encoding="utf-8")
            data["message"] = data["msg"]
            data["asctime"] = time.strftime(date_fmt, time.localtime(data["created"]))
            file.write(fmt % data)
        except Exception as err:
            LOG.error(err)
