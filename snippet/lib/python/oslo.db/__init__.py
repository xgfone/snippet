# encoding: utf-8
from oslo.config import cfg
from oslo.db import options
from oslo.db import api as db_api

# There must be a function `get_backend` in 'api'.
_BACKEND_MAPPING = {'sqlalchemy': 'api'}
_IMPL = None


def _parse_config(config):
    result = {}

    if not config:
        return result

    if isinstance(config, dict):
        result['connection'] = config['sql_connection']
    else:
        result['connection'] = config.sql_connection

    return result


def get_impl(config=None, CONF=None, backend_mapping=None, lazy=False):
    CONF = CONF if CONF else cfg.CONF
    backend_mapping = backend_mapping if backend_mapping else _BACKEND_MAPPING
    config = _parse_config(config)

    if config:
        CONF.register_opts(options.database_opts, 'database')
        CONF.set_override('connection', config['connection'], group='database')

        return db_api.DBAPI.from_config(CONF, backend_mapping=_BACKEND_MAPPING, lazy=lazy, register_opts=False)
    else:
        global _IMPL
        if _IMPL:
            return _IMPL

        _IMPL = db_api.DBAPI.from_config(CONF, backend_mapping=_BACKEND_MAPPING, lazy=lazy, register_opts=False)
        return _IMPL
