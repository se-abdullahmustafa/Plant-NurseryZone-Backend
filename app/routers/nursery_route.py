from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.DBHandler import get_db
from app.repository.nursery_repository import get_nursery_requests,toggle_nursery_request
from typing import List

router=APIRouter()

@router.get("/nursery/request",response_class=JSONResponse)
def get_nurseries_request(pending_request:bool=True,skip:int=0,limit:int=20,db:Session=Depends(get_db)):
    return get_nursery_requests(db=db,pending_request=pending_request,skip=skip,limit=limit)
@router.post("/nursery/request",response_class=JSONResponse)
def change_nursery_request_status(nursery_id:int,is_accepted:bool,db:Session=Depends(get_db)):
    return toggle_nursery_request(db=db,nursery_id=nursery_id,is_accepted=is_accepted)