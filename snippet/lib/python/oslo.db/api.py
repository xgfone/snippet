# encoding: utf-8
from oslo.config import cfg
import time
import logging

from oslo.db.sqlalchemy import session
from models import UserProject
from models import ContainerCostDetails
from models import ContainerBillInfo

_FACADE = None
CONF = cfg.CONF
LOG = logging.getLogger(__name__)


def get_backend():
    return DBOperate()


def _create_facade_lazily():
    global _FACADE
    if _FACADE is None:
        _FACADE = session.EngineFacade.from_config(CONF, register_opts=False)
    return _FACADE


def get_session():
    if not _FACADE:
        _create_facade_lazily()
    return _FACADE.get_session()


class DBOperate():
    def __init__(self):
        self.session = get_session()

    def replace_project_user(self, project_id):
        item = self.session.query(UserProject).filter(UserProject.project_id == project_id).first()
        if item:
            return item.user_id

    def newitem_container_cost(self, project_id, container_obj, update_time=None):
        _TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        entry = ContainerCostDetails(project_id=project_id, container_id=container_obj['container_id'],
                                     container_name=container_obj['container_name'],
                                     container_cost='0.00',
                                     container_zone=container_obj['zonename'],
                                     runtime='0',
                                     status='active',
                                     flavor_id=container_obj['flavor_id'],
                                     update_time=_TIME)
        entry.save(self.session)

        container = ContainerBillInfo(project_id=project_id,
                                      container_id=container_obj['container_id'],
                                      container_name=container_obj['container_name'],
                                      container_zone=container_obj['zonename'],
                                      status='active',
                                      flavor_id=container_obj['flavor_id'],
                                      created_at=_TIME)
        container.save(self.session)

    def set_container_status(self, project_id, container_id, status):
        entry = self.session.query(ContainerBillInfo).\
            filter(ContainerBillInfo.project_id == project_id).\
            filter(ContainerBillInfo.container_id == container_id).first()
        if entry:
            entry.update({'status': status})
            self.session.flush()
