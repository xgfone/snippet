# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals, division

import logging

from sqlalchemy.ext.declarative import declarative_base
from oslo_db.sqlalchemy import models
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import fun

LOG = logging.getLogger(__name__)
BASE = declarative_base()


class TestData(models.ModelBase, BASE):
    __tablename__ = 'test_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String(256), nullable=False)
    create_time = Column(DateTime, server_default=func.now(), nullable=False)

    def __init__(self, *args, **kwargs):
        super(TestData, self).__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)

def create_tables(engine=None):
    if not engine:
        try:
            import sys
            engine = sys.argv[1]
        except IndexError:
            engine = "sqlite:///:memory:"
    engine = create_engine(engine, echo=True)
    BASE.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables("sqlite:///:memory:")
