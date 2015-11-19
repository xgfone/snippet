# coding: utf-8
import threading
from oslo_db.sqlalchemy import session as db_session

_ENGINE_FACADE = {}
_LOCK = threading.Lock()


def _create_facade(conf_group):
    # This fragment is copied from oslo.db
    return db_session.EngineFacade(
        sql_connection=conf_group.connection,
        slave_connection=conf_group.slave_connection,
        sqlite_fk=False,
        autocommit=True,
        expire_on_commit=False,
        mysql_sql_mode=conf_group.mysql_sql_mode,
        idle_timeout=conf_group.idle_timeout,
        connection_debug=conf_group.connection_debug,
        max_pool_size=conf_group.max_pool_size,
        max_overflow=conf_group.max_overflow,
        pool_timeout=conf_group.pool_timeout,
        sqlite_synchronous=conf_group.sqlite_synchronous,
        connection_trace=conf_group.connection_trace,
        max_retries=conf_group.max_retries,
        retry_interval=conf_group.retry_interval)


def _create_facade_lazily(facade, conf_group):
    global _LOCK, _ENGINE_FACADE
    if _ENGINE_FACADE.get(facade) is None:
        with _LOCK:
            if _ENGINE_FACADE.get(facade) is None:
                _ENGINE_FACADE[facade] = _create_facade(conf_group)
    return _ENGINE_FACADE[facade]


def get_engine(conf_group, use_slave=False):
    """Get the Engine object.

    If `use_slave` is True, the operations of read and write are detached.
    """
    facade = _create_facade_lazily(conf_group._group.name, conf_group)
    return facade.get_engine(use_slave=use_slave)


def get_session(conf_group, use_slave=False, **kwargs):
    """Get the Session object.

    If `use_slave` is True, the operations of read and write are detached.
    """
    facade = _create_facade_lazily(conf_group._group.name, conf_group)
    return facade.get_session(use_slave=use_slave, **kwargs)
