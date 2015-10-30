# encoding: utf-8

DEFAULT_LOGGING = {
    "version": 1,
    "incremental": False,  # Replaces the existing configuration
    "root": {
        "level": "DEBUG",
        "propagate": 0,
        "handlers": ["file", "console"],
        "filters": [],
    },
    "loggers": {
        "default": {
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
            "filename": "/var/log/{PROJECT}/{PROJECT}.log",
            "when": "D",  # Backup once each day.
            "interval": 1,
            "backupCount": 31,  # The total number to backup.
        }
    }
}


def get_config(project, config=None):
    import copy
    _config = copy.deepcopy(DEFAULT_LOGGING)

    file_handler = _config["handlers"]["file"]
    file_handler["filename"] = file_handler["filename"].format(PROJECT=project)
    _config["loggers"][project] = _config["loggers"]["default"]

    if not isinstance(config, dict):
        return _config

    version = config.get("version", None)
    if version is not None:
        _config["version"] = version

    incremental = config.get("incremental", None)
    if incremental is not None:
        _config["incremental"] = incremental

    root = config.get("root", None)
    if root is not None:
        _config["root"] = root

    loggers = config.get("loggers", {})
    for k, v in loggers.items():
        _config["loggers"][k] = v

    formatters = config.get("formatters", {})
    for k, v in formatters.items():
        _config["formatters"][k] = v

    handlers = config.get("handlers", {})
    for k, v in handlers.items():
        _config["handlers"][k] = v

    filters = config.get("filters", {})
    for k, v in filters.items():
        _config["filters"][k] = v

    return _config
