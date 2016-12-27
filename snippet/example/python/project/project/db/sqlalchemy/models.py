# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals, division

import logging

from sqlalchemy.ext.declarative import declarative_base
from oslo_db.sqlalchemy import models
from sqlalchemy import Column, String, Integer

LOG = logging.getLogger(__name__)
BASE = declarative_base()


class TestData(models.ModelBase, BASE):
    __tablename__ = 'test_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String(256), nullable=False)

    def __init__(self, *args, **kwargs):
        super(TestData, self).__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)
