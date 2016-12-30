# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals, division

import sys
import logging

from oslo_config import cfg
from oslo_db import options as oslo_db_options

from .base import get_session, get_engine
from . import models

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

CONF.register_opts(oslo_db_options.database_opts, 'database')

# For Test
oslo_db_options.set_defaults(CONF, connection="sqlite:///:memory:")
DB_INIT = False


def get_backend():
    """The backend is this module itself."""
    # For Test
    global DB_INIT
    if not DB_INIT:
        models.TestData.metadata.create_all(get_engine(CONF.database))
        DB_INIT = True

    return sys.modules[__name__]


###########################################################
# Utility Functions
def get_attr(obj, name):
    if hasattr(obj, name):
        return getattr(obj, name)
    return obj[name]


class RowRroxy(object):
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


###############################################################
# API Interfaces
def get_data(_id):
    model = models.TestData
    session = get_session(CONF.database)
    query = session.query(model)
    obj = query.filter_by(id=_id).first()
    if obj:
        return {
            "id": obj.id,
            "data": obj.data
        }
    else:
        return None


def set_data(data):
    model = models.TestData
    session = get_session(CONF.database)
    obj = model(data=data)
    obj.save(session)
    return {
        "id": obj.id,
    }
