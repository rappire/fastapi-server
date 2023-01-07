import sys

sys.path.append("..")
from fastapi import APIRouter, Depends
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from sqlalchemy import func

router = APIRouter(
    prefix="", tags=["step0"], responses={401: {"user": "Not authorized"}}
)
models.Base.metadata.create_all(bind=engine)


class Name(BaseModel):
    name: str = Field(min_length=1)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/step0")
async def get_name(db: Session = Depends(get_db)):
    name = db.query(models.Name).filter().all()
    namelist = []
    for i in name:
        N = Name(name=i.name)
        namelist.append(N)
    return namelist


@router.get("/id")
async def get_id(db: Session = Depends(get_db)):
    try:
        id = (
            max(
                db.query(func.max(models.Schedule.id)).first()[0],
                db.query(func.max(models.Plan_name.id)).first()[0],
            )
            + 1
        )
    except:
        id = 1
    return id
