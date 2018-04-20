# -*- encoding: utf-8 -*-

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import TextClause


class DB(object):
    """Manager the DB connection."""

    def __init__(self, write_connection, read_connection=None, autocommit=True,
                 expire_on_commit=False, echo=False, encoding=str("utf8"),
                 poolclass=None, pool=None, min_pool_size=2, max_pool_size=5,
                 pool_timeout=30, idle_timeout=3600, base=None):

        write_connection = self._fix_charset(write_connection, encoding)
        if read_connection:
            read_connection = self._fix_charset(read_connection, encoding)

        kwargs = {
            "echo": echo,
            "encoding": encoding,
            "poolclass": poolclass,
            "pool": pool,
            "pool_size": min_pool_size,
            "pool_timeout": pool_timeout if pool_timeout else None,
            "pool_recycle": idle_timeout,
            "max_overflow": max_pool_size - min_pool_size,
            "convert_unicode": True,
        }

        self._base = base
        self._autocommit = autocommit
        self._expire_on_commit = expire_on_commit

        self._write_engine = self._create_engine(write_connection, kwargs)
        self._write_session_cls = self._get_session_cls(self._write_engine)

        if read_connection:
            self._read_engine = self._create_engine(read_connection, kwargs)
            self._read_session_cls = self._get_session_cls(self._read_engine)
        else:
            self._read_engine = self._write_engine
            self._read_session_cls = self._write_session_cls

    def _fix_charset(self, connection, encoding):
        if "mysql" in connection and "charset=" not in connection:
            if "?" in connection:
                return "%s&charset=%s" % (connection, encoding)
            return "%s?charset=%s" % (connection, encoding)
        return connection

    def _create_engine(self, connection, kwargs):
        if connection.startswith("sqlite:///"):
            kwargs.pop("pool_size", None)
            kwargs.pop("pool_timeout", None)
            kwargs.pop("max_overflow", None)
        return create_engine(connection, **kwargs)

    def _get_session_cls(self, engine):
        return sessionmaker(bind=engine, autocommit=self._autocommit,
                            expire_on_commit=self._expire_on_commit)

    def create_tables(self, base=None):
        (base or self._base).metadata.create_all(self._write_engine)

    def get_write_session(self):
        return self._write_session_cls()

    def get_read_session(self):
        return self._read_session_cls()

    def get_session(self):
        return self.get_write_session()

    def execute(self, sql, session=None, **kwargs):
        if not isinstance(sql, TextClause):
            sql = text(sql)
        return (session or self.get_session()).execute(sql, kwargs)

    def fetchall(self, sql, **kwargs):
        return self.execute(sql, self.get_read_session(), **kwargs).fetchall()

    def fetchone(self, sql, **kwargs):
        return self.execute(sql, self.get_read_session(), **kwargs).fetchone()

    def first(self, sql, **kwargs):
        return self.execute(sql, self.get_read_session(), **kwargs).first()
