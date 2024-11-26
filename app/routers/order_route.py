from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.DBHandler import get_db
from app.schemas.order import *
from app.repository.order_repository import *
from typing import List

router=APIRouter()

@router.post("/order",response_class=JSONResponse)
async def place_order(order:OrderCreate,db:Session=Depends(get_db)):
    return await add_order(db,order)
@router.get("/order",response_class=JSONResponse)
async def get_orders(nursery_id:int,skip:int=0,limit:int=20,db:Session=Depends(get_db)):
    return await get_all_order(db,nursery_id,skip,limit)