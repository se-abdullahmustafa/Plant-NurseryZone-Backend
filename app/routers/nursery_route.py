from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.DBHandler import get_db
from app.schemas.nursery import NurseryCreate,NurseryResponse

router=APIRouter()

