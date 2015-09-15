# coding: utf-8

from oslo_config import cfg
from oslo_db import concurrency
from oslo_log import log as logging

LOG = logging.getLogger(__name__)

CONF = cfg.CONF
_BACKEND_MAPPING = {'sqlalchemy': "oslodb.sqlalchemy.api"}

IMPL = concurrency.TpoolDbapiWrapper(CONF, backend_mapping=_BACKEND_MAPPING)


####################################
# API Interface
def get_user_info(username):
    IMPL.get_user_info(username)
