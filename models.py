from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base

# extend_existing=True


class Order(Base):
    __tablename__ = "order"
    orderid = Column(Integer, primary_key=True)
    companyid: Column(String(50), nullable=False)
    itemid: Column(String(50), nullable=False)
    date: Column(String(50), nullable=False)
    num: Column(Integer, nullable=False)
    drawcd: Column(Boolean, default=False, nullable=False)
    urgency: Column(Boolean, default=False, nullable=False)


class Machine(Base):
    __tablename__ = "machine"
    machine = Column(String(50), primary_key=True)
    companyid = Column(String(50))


class Name(Base):
    __tablename__ = "name"
    name = Column(String(50), primary_key=True)


class Plan(Base):
    __tablename__ = "plan"
    planid = Column(Integer, primary_key=True, autoincrement=True)
    companyid = Column(String(50), nullable=False)
    itemid = Column(String(50), nullable=False)
    estbl = Column(Boolean, default=False, nullable=False)
    planlist = Column(String(1000), nullable=True)


class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    companyid = Column(String(50), nullable=False)
    itemid = Column(String(50), nullable=False)
    machine = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    color = Column(String(50), nullable=False)
