from fastapi import APIRouter,Depends
from app.repository.feedback_repository import *
from fastapi.responses import JSONResponse
from app.schemas.feedback import FeedbackCreate
from sqlalchemy.orm import Session
from app.DBHandler import get_db


router=APIRouter()

@router.post("/feedback",response_class=JSONResponse)
async def post_feedback(feedback:FeedbackCreate,db:Session=Depends(get_db)):
    return await add_feedback(db,feedback)
@router.get("/feedback",response_class=JSONResponse)
async def get_feeback(plant_id:int,db:Session=Depends(get_db)):
    return await get_feedback_by_plant_id(db,plant_id)
@router.get("/feedback/{nursery_id}",response_class=JSONResponse)
async def get_feeback(nursery_id:int,db:Session=Depends(get_db)):
    return await get_feedback_by_nursery_id(db,nursery_id)