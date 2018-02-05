from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import TextClause


class DB(object):
    """Manager the DB connection."""

    class _Session:
        def __init__(self, s):
            self._session = s

        def __getattr__(self, name):
            return getattr(self._session, name)

        def __del__(self):
            self.close()

        def close(self):
            if self._session:
                self._session.close()
                self._session = None

    def __init__(self, connection, timeout=240):
        self._connection = connection
        self._timeout = timeout

        self._engine = create_engine(connection, pool_recycle=timeout)
        self._session_cls = sessionmaker(bind=self._engine, autocommit=True)

    def get_session(self):
        return self._Session(self._session_cls())

    def execute(self, sql, **kwargs):
        if not isinstance(sql, TextClause):
            sql = text(sql)
        return self.get_session().execute(sql, kwargs)

    def fetchall(self, sql, **kwargs):
        return self.execute(sql, **kwargs).fetchall()

    def fetchone(self, sql, **kwargs):
        return self.execute(sql, **kwargs).fetchone()

    def first(self, sql, **kwargs):
        return self.execute(sql, **kwargs).first()
