import sys

sys.path.append("..")
from fastapi import APIRouter, Depends, HTTPException, status
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List

router = APIRouter(
    prefix="/step3", tags=["step3"], responses={401: {"user": "Not authorized"}}
)
models.Base.metadata.create_all(bind=engine)


class Schedule(BaseModel):

    id: int = Field()
    companyid: str = Field(min_length=1)
    itemid: str = Field(min_length=1)
    machine: str = Field(min_length=1)
    name: str = Field(min_length=1)
    start: str = Field(min_length=1)
    end: str = Field(min_length=1)
    color: str = Field(min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "companyid": "company1",
                "itemid": "item1",
                "machine": "machine1",
                "name": "name1",
                "start": "2023-01-02",
                "end": "2023-01-05",
                "color": "red",
            }
        }


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("")
async def get_schedule(itemid: str, companyid: str, db: Session = Depends(get_db)):
    schedule = (
        db.query(models.Schedule)
        .filter(
            models.Schedule.itemid == itemid and models.Schedule.companyid == companyid
        )
        .all()
    )
    machine = (
        db.query(models.Machine).filter(models.Machine.companyid == companyid).all()
    )
    scheduledict = {}
    for i in machine:
        scheduledict[i.machine] = []
    for i in schedule:
        print(i.machine)
        i.start = i.start.strftime("%Y-%m-%d %H:%M")
        i.end = i.end.strftime("%Y-%m-%d %H:%M")
        scheduledict[i.machine].append(i)
    return scheduledict


@router.post("")
async def post_schedule(schedule: List[Schedule], db: Session = Depends(get_db)):
    for i in schedule:
        S = db.query(models.Schedule).filter(models.Schedule.id == i.id).first()
        if S is None:
            S = models.Schedule()
        S.id = i.id
        S.companyid = i.companyid
        S.itemid = i.itemid
        S.machine = i.machine
        S.name = i.name
        S.color = i.color
        S.start = i.start
        S.end = i.end
        db.add(S)
    db.commit()
    return


# 1개만 put
@router.put("_1")
async def put_schedule(schedule: Schedule, db: Session = Depends(get_db)):
    S = db.query(models.Schedule).filter(models.Schedule.id == schedule.id).first()
    if S is None:
        raise get_exception()
    S.machine = schedule.machine
    S.name = schedule.name
    S.color = schedule.color
    S.start = schedule.start
    S.end = schedule.end
    db.add(S)
    db.commit()
    return


# 리스트 put
@router.put("_2")
async def put_schedule(schedule: List[Schedule], db: Session = Depends(get_db)):
    for i in schedule:
        S = db.query(models.Schedule).filter(models.Schedule.id == i.id).first()
        if S is None:
            raise get_exception()
        S.machine = i.machine
        S.name = i.name
        S.color = i.color
        S.start = i.start
        S.end = i.end
        db.add(S)
    db.commit()
    return


def get_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="There is no data",
    )
    return credentials_exception
