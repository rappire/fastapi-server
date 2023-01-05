import sys

sys.path.append("..")
from fastapi import APIRouter, Depends, HTTPException, status
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from typing import List

router = APIRouter(
    prefix="/step2", tags=["step2"], responses={401: {"user": "Not authorized"}}
)
models.Base.metadata.create_all(bind=engine)


class Plan(BaseModel):
    id: int = Field()
    companyid: str = Field(min_length=1)
    itemid: str = Field(min_length=1)
    name: str = Field(min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "companyid": "company1",
                "itemid": "item1",
                "name": "name1",
            }
        }


class Plan_name(BaseModel):
    planid: int = Field()
    id: int = Field()
    name: str = Field(min_length=1)
    idx: int = Field()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("")
def get_plan(itemid: str, companyid: str, db: Session = Depends(get_db)):
    plan = (
        db.query(models.Plan)
        .filter(models.Plan.itemid == itemid and models.Plan.companyid == companyid)
        .first()
    )
    if plan is None:
        return None
    planid = plan.planid
    plan_name = (
        db.query(models.Plan_name).filter(models.Plan_name.planid == planid).all()
    )
    plan_name.sort(key=lambda x: x.idx)
    planlist = []
    for i in plan_name:
        P = Plan(companyid=plan.companyid, itemid=plan.itemid, id=i.id, name=i.name)
        planlist.append(P)
    return planlist


@router.post("")
def post_plan(plan: List[Plan], db: Session = Depends(get_db)):
    plan_model = models.Plan()
    plan_model.companyid = plan[0].companyid
    plan_model.itemid = plan[0].itemid
    try:
        id = db.query(func.max(models.Plan.planid)).first()[0] + 1
    except:
        id = 1
    plan_model.planid = id
    db.add(plan_model)
    for i, P in enumerate(plan):
        plan_name_model = models.Plan_name()
        plan_name_model.idx = i
        plan_name_model.id = P.id
        plan_name_model.name = P.name
        plan_name_model.planid = id
        db.add(plan_name_model)
    db.commit()
    return


def get_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="There is no data",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception
