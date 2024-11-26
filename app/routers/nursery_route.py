from fastapi import APIRouter,Depends, UploadFile,File,Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.DBHandler import get_db
from app.repository.nursery_repository import *
from app.schemas.plant import PlantResponse
from typing import Optional,List

router=APIRouter()

@router.get("/nursery/request",response_class=JSONResponse)
def get_nurseries_request(pending_request:bool=True,skip:int=0,limit:int=20,db:Session=Depends(get_db)):
    return get_nursery_requests(db=db,pending_request=pending_request,skip=skip,limit=limit)
@router.post("/nursery/request",response_class=JSONResponse)
def change_nursery_request_status(nursery_id:int,is_accepted:bool,db:Session=Depends(get_db)):
    return toggle_nursery_request(db=db,nursery_id=nursery_id,is_accepted=is_accepted)
@router.post("/nursery/plant",response_class=JSONResponse)
async def add_plant(nursery_id: int=Form(...),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: str = Form(...),
    stock: int = Form(0),
    image: UploadFile = File(...),  # Made required with ...
    db:Session=Depends(get_db)):
    return await add_new_plant(db,nursery_id,name,description,price,stock,image)
@router.get("/nursery/plants",response_model=List[PlantResponse])
async def get_plants(skip:int=0,limit:int=20,db:Session=Depends(get_db)):
    return await get_all_plant(db,skip,limit)
@router.get("/nursery/plant",response_model=PlantResponse)
async def get_plant(plant_id:int,db:Session=Depends(get_db)):
    return await get_plant_by_id(db,plant_id)
@router.delete("/nursery/plant",response_class=JSONResponse)
async def delete_plant(plant_id:int,db:Session=Depends(get_db)):
    return await remove_plant(db,plant_id)
@router.put("/nursery/plant",response_class=JSONResponse)
async def update_plant(plant_id: int=Form(...),
    name: str = Form(...),
    description: str = Form(...),
    price: str = Form(...),
    stock: int = Form(...),
    image: UploadFile = File(...),  # Made required with ...
    db:Session=Depends(get_db)):
    return await update_plant_by_id(db,plant_id,name,description,price,stock,image)
@router.put("/nursery/stock",response_class=JSONResponse)
async def update_stocke(plant_id:int,stock:int,db:Session=Depends(get_db)):
    return await update_plant_stock(db,plant_id,stock)
@router.put("/nursery/price",response_class=JSONResponse)
async def update_price(plant_id:int,price:str,db:Session=Depends(get_db)):
    return await update_plant_price(db,plant_id,price)