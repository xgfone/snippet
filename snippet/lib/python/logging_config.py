# encoding: utf-8

PROJECT = "PROJECT"

LOGGING = {
    "version": 1,
    "incremental": False,  # Replaces the existing configuration
    "root": {
        "level": "DEBUG",
        "propagate": 0,
        "handlers": ["file", "console"],
        "filters": [],
    },
    "loggers": {
        PROJECT: {
            "level": "INFO",
            "propagate": 0,
            "handlers": ["file", "console"],
            "filters": [],
        }
    },
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "filters": {
        "all": {
            "name": ""
        }
    },
    "handlers": {
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "filters": [],
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "simple",
            "filters": [],

            # Arguments of handler
            "filename": "/var/log/{PROJECT}/{PROJECT}.log".format(PROJECT=PROJECT),
            "when": "D",  # Backup once each day.
            "interval": 1,
            "backupCount": 31,  # The total number to backup.
        }
    }
}
