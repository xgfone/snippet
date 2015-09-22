# coding: utf-8

from oslo_config import cfg
from oslo_db import concurrency
from oslo_log import log as logging

CONF = cfg.CONF
LOG = logging.getLogger(__name__)
_BACKEND_MAPPING = {'sqlalchemy': "{PROJECT}.db.sqlalchemy.api"}

IMPL = concurrency.TpoolDbapiWrapper(CONF, backend_mapping=_BACKEND_MAPPING)
# import threading
# from oslo_db import api
#
# _IMPL = None
# _LOCK = threading.Lock()
# def get_api():
#     global _IMPL, _LOCK
#     if not _IMPL:
#         with _LOCK:
#             if not _IMPL:
#                 _IMPL = api.DBAPI.from_config(conf=CONF,
#                                               backend_mapping=_BACKEND_MAPPING)
#     return _IMPL


####################################
# API Interface
def insert_data(*args, **kwargs):
    return IMPL.insert_data(*args, **kwargs)


def get_all_datas(*args, **kwargs):
    return IMPL.get_all_datas(*args, **kwargs)
