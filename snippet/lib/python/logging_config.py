# encoding: utf-8

DEFAULT_LOGGING = {
    "version": 1,
    "incremental": False,  # Replaces the existing configuration
    "root": {
        "level": "DEBUG",
        "propagate": 0,
        "handlers": ["file"],
        "filters": [],
    },
    "loggers": {
        "default": {
            "level": "INFO",
            "propagate": 0,
            "handlers": ["file"],
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
            "when": "midnight",  # Backup once each day.
            "interval": 1,
            "backupCount": 31,  # The total number to backup.
        }
    }
}


def get_config(project, config=None, filepath=None, console=False):
    import copy
    _config = copy.deepcopy(DEFAULT_LOGGING)

    f = _config["handlers"]["file"]
    f["filename"] = filepath if filepath else f["filename"].format(PROJECT=project)

    if console:
        _config["root"]["handlers"].append("console")
        _config["loggers"]["default"]["handlers"].append("console")
    _config["loggers"][project] = _config["loggers"]["default"]

    if not isinstance(config, dict):
        return _config

    data1 = ("version", "incremental", "root")
    for d in data1:
        v = config.get(d, None)
        if v is not None:
            _config[d] = v

    data2 = ("loggers", "formatters", "handlers", "filters")
    for d in data2:
        for k, v in config.get(d, {}).items():
            if d in _config:
                _config[d].update(v)
            else:
                _config[d][k] = copy.deepcopy(v)

    return _config


def setup_logging(project, config=None, filepath=None, console=False):
    from logging.config import dictConfig
    config = get_config(project, config, filepath, console)
    dictConfig(config)
