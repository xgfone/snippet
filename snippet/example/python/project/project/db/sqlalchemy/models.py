# coding: utf-8
import logging

from sqlalchemy.ext.declarative import declarative_base
from oslo_db.sqlalchemy import models
from sqlalchemy import Column, String

_BASE = declarative_base()
LOG = logging.getLogger(__name__)


class BASE(models.ModelBase, models.TimestampMixin):
    pass


class UserInfo(_BASE, BASE):
    __tablename__ = "user_info"

    user_id = Column(String(32), primary_key=True, nullable=False)
    user_name = Column(String(128))
    email = Column(String(128))
    phone = Column(String(128))

    def __init__(self, *args, **kwargs):
        super(UserInfo, self).__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)
