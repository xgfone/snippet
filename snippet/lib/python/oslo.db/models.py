# encoding: utf-8
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from oslo.db.sqlalchemy import models

BASE = declarative_base()


class ContainerBillInfo(models.ModelBase,
                        #models.TimestampMixin,
                        #models.SoftDeleteMixin,
                        BASE):

    __tablename__ = 'container_bill_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(36), nullable=False)
    container_id = Column(String(36), nullable=False)
    status = Column(String(10))
    flavor_id = Column(String(36))
    container_name = Column(String(255))
    container_zone = Column(String(50))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class ContainerCostDetails(models.ModelBase, BASE):
    __tablename__ = 'container_cost_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(36), nullable=False)
    container_id = Column(String(36), nullable=False)
    container_name = Column(String(255))
    container_cost = Column(String(20))
    container_zone = Column(String(50))
    runtime = Column(String(10))
    status = Column(String(10))
    flavor_id = Column(String(36))
    update_time = Column(DateTime)


class UserProject(models.ModelBase, BASE):
    __tablename__ = "user_project"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), nullable=False)
    project_id = Column(String(36), nullable=False)
    zone_id = Column(String(36), nullable=False)
    total_instances = Column(Integer)
