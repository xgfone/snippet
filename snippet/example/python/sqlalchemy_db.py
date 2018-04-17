# -*- encoding: utf-8 -*-

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import TextClause


class DB(object):
    """Manager the DB connection."""

    def __init__(self, write_connection, read_connection=None, autocommit=True,
                 expire_on_commit=False, echo=False, encoding=str("utf8"),
                 poolclass=None, pool=None, min_pool_size=1, max_pool_size=5,
                 pool_timeout=10, idle_timeout=3600):

        if "charset=" not in write_connection:
            if "?" in write_connection:
                write_connection = "%s&charset=%s" % (write_connection, encoding)
            else:
                write_connection = "%s?charset=%s" % (write_connection, encoding)

        if read_connection and "charset=" not in read_connection:
            if "?" in read_connection:
                read_connection = "%s&charset=%s" % (read_connection, encoding)
            else:
                read_connection = "%s?charset=%s" % (read_connection, encoding)

        kwargs = {
            "echo": echo,
            "encoding": encoding,
            "poolclass": poolclass,
            "pool": pool,
            "pool_size": min_pool_size,
            "pool_timeout": pool_timeout,
            "pool_recycle": idle_timeout,
            "max_overflow": max_pool_size - min_pool_size,
            "convert_unicode": True,
        }
        self._kwargs = kwargs
        self._autocommit = autocommit
        self._expire_on_commit = expire_on_commit

        self._write_engine = create_engine(write_connection, **kwargs)
        self._write_session_cls = self._get_session_cls(self._write_engine)

        if read_connection:
            self._read_engine = create_engine(read_connection, **kwargs)
            self._read_session_cls = self._get_session_cls(self._read_engine)
        else:
            self._read_engine = self._write_engine
            self._read_session_cls = self._write_session_cls

    def _get_session_cls(self, engine):
        return sessionmaker(bind=engine, autocommit=self._autocommit,
                            expire_on_commit=self._expire_on_commit)

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
