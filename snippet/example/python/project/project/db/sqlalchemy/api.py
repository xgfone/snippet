# coding: utf-8
from __future__ import absolute_import, print_function

import sys

from oslo_config import cfg
from oslo_db import options as oslo_db_options
from oslo_db.sqlalchemy import utils as sqlalchemyutils
from oslo_log import log as logging

from .base import get_session
from . import models

LOG = logging.getLogger(__name__)

CONF = cfg.CONF
CONF.register_opts(oslo_db_options.database_opts, 'database')
CONF.register_opts(oslo_db_options.database_opts, 'api_database')


def get_backend():
    """The backend is this module itself."""
    return sys.modules[__name__]


###########################################################
# Utility Functions
def get_attr(obj, name):
    if hasattr(obj, name):
        return getattr(obj, name)
    return obj[name]


class _RowRroxy(object):
    def __init__(self, obj, *args, **kwargs):
        self._obj = obj
        self._args = args
        self._kwargs = kwargs

    def __getattr__(self, name):
        return get_attr(self._obj, name)

    def __eq__(self, other):
        for k in iter(self._obj):
            if getattr(self._obj, k) != getattr(other._obj, k):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


def model_query(model, session):
    return sqlalchemyutils.model_query(model, session)


###############################################################
# API Interfaces
def get_all_datas():
    session = get_session(CONF.api_database)
    model = models.UserInfo
    query = model_query(model, session)
    return query.all()


def insert_data(*args, **kwargs):
    def _get_obj(*args, **kwargs):
        return models.UserInfo(*args, **kwargs)

    session = get_session(CONF.api_database)
    obj = _get_obj(*args, **kwargs)
    obj.save(session)
