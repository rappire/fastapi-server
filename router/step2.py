import sys

sys.path.append("..")
from fastapi import APIRouter, Depends, HTTPException, status
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import desc
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
async def get_plan(itemid: str, companyid: str, db: Session = Depends(get_db)):
    plan = (
        db.query(models.Plan)
        .filter(models.Plan.itemid == itemid and models.Plan.companyid == companyid)
        .first()
    )
    if plan is None:
        return None
    planlist = []
    for i in plan.planlist[:-1].split(";"):
        id, name = i.split(",")
        P = Plan(companyid=companyid, itemid=itemid, id=id, name=name)
        planlist.append(P)
    return planlist


@router.post("")
async def post_plan(plan: List[Plan], db: Session = Depends(get_db)):
    P = (
        db.query(models.Plan)
        .filter(
            models.Plan.companyid == plan[0].companyid
            and models.Plan.itemid == plan[0].itemid
        )
        .first()
    )
    if P is None:
        P = models.Plan()
        P.companyid = plan[0].companyid
        P.itemid = plan[0].itemid
    string = ""
    for i in plan:
        string += f"{i.id},{i.name};"
    P.planlist = string
    db.add(P)
    db.commit()
