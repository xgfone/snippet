# coding: utf-8
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from oslo.db.sqlalchemy import models


class APIBASE(models.ModelBase, models.TimestampMixin):
    pass


BASE = declarative_base()


class UserInfo(BASE):

    __tablename__ = 'user_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(40), nullable=False)
    password = Column(String(40), nullable=False)
    email = Column(String(40), nullable=True)
