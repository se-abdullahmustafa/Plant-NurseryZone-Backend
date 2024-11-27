from datetime import datetime
from pathlib import Path
import shutil
from sqlalchemy import select
from app.schemas.nursery import NurseryCreate,NurseryResponse
from app.models.Nurseries import Nurseries as NurseryModel
from app.models.User import User as UserModel
from sqlalchemy.orm import Session
from fastapi import HTTPException,UploadFile,File,Form
from typing import Optional
from app.models.Plant import Plant as PlantModel
import os

UPLOAD_DIR = Path("static/plant_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True) 
# def register_nursery(db:Session,nursery:NurseryCreate):
#     db_nursery=NurseryModel(user_id=nursery.user_id)
#     db.add(db_nursery)
#     db.commit()
#     db.refresh(db_nursery)
#     return db_nursery
async def get_nursery_by_user_id(db:Session,user_id:int):
    nursery=db.query(NurseryModel).filter(NurseryModel.user_id==user_id).first()
    if not nursery:
        raise HTTPException(status_code=404,detail="Nursery not found.")
    return nursery
async def get_nursery(db:Session,nursery_id:int):
    nursery= db.query(NurseryModel).filter(NurseryModel.nursery_id==nursery_id).filter(NurseryModel.status=="Accepted").first()
    if not nursery_id:
        raise HTTPException(status_code=404,detail="Nursery not found")
    return nursery
def get_nursery_requests(db:Session,pending_request:bool=True,skip:int=0,limit:int=20):
    nurseries = db.query(NurseryModel,UserModel).join(UserModel,NurseryModel.user_id==UserModel.user_id).filter(NurseryModel.status== "Pending" if pending_request else NurseryModel.status=="Accepted").order_by(UserModel.user_id).offset(skip).limit(limit=limit).all()
    if nurseries is None or len(nurseries)==0:
        raise HTTPException(status_code=404,detail="No nurseries request found")
    result = []
    for nursery, user in nurseries:
        nursery_dict = {
            "nursery_id": nursery.nursery_id,
            "name": user.name,
            "email": user.email,
            "address":user.address,
            "contact_number":user.contact_number,
            "status": nursery.status,
            "user_id": user.user_id,
            
        }
        result.append(nursery_dict)
    return result
def toggle_nursery_request(db:Session, nursery_id:int,is_accepted:bool):
    db_nursery=db.query(NurseryModel).filter(NurseryModel.nursery_id==nursery_id).first()
    if db_nursery is None:
        raise HTTPException(status_code=404,detail="Nursery not found")
    if is_accepted:
        db_nursery.status="Accepted"
    else:
        db_nursery.status="Rejected"
    db.commit()
    return {"message":"Status has been changed successfully."}
async def update_plant_stock(db:Session,plant_id:int,stock:int):
    plant=await get_plant_by_id(db,plant_id)
    plant.stock+=stock
    db.commit()
    db.refresh(plant)
    return {"Stock Updated Successfully."}
async def decrease_stock(db:Session,stock:int,plant_id:int):
    plant=await get_plant_by_id(db,plant_id)
    plant.stock-=stock
    db.commit()
    db.refresh(plant)
    return plant
async def update_plant_price(db:Session,plant_id:int,price:str):
    plant=await get_plant_by_id(db,plant_id)
    plant.price=price
    db.commit()
    db.refresh(plant)
    return {"price updated Successfully."}

async def update_plant_by_id(db:Session,plant_id:int,name:str,
              description:str,
              price:str,
              stock:Optional[int],
              image:str):
    plant=await get_plant_by_id(db,plant_id)
    plant.name=name
    plant.description=description
    plant.price=price
    plant.stock=stock
    if image is not None:
        await validate_image(image)
        image_url=await save_image(image)
        plant.image_url=image_url
    db.commit()
    db.refresh(plant)
    return {"Plant updated Successfully."}    

async def remove_plant(db:Session,plant_id:int):
    plant=await get_plant_by_id(db,plant_id)
    try:
        db.delete(plant)
        db.commit()
        return {"Plant Deleted Successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
        

async def get_plant_by_id(db:Session,plant_id:int):
    plant=db.query(PlantModel).filter(PlantModel.plant_id==plant_id).first()
    if not plant:
        raise HTTPException(status_code=404,detail="Plant not found")
    return plant

async def get_all_plant(db:Session,nursery_id:int,skip:int=0,limit:int=20):
    nursery=await get_nursery_by_user_id(db,nursery_id)
    plants=db.query(PlantModel).filter(PlantModel.nursery_id==nursery.nursery_id).order_by(PlantModel.plant_id).offset(skip).limit(limit).all()
    if not plants:
         raise  HTTPException(status_code=404,detail="No plant found.")
    return plants 

async def add_new_plant(db:Session,
              nursery_id:int,
              name:str,
              description:str,
              price:str,
              stock:Optional[int],
              image:str):
    nursery=await get_nursery_by_user_id(db=db,nursery_id=nursery_id)
    await validate_image(image)
    image_url=await save_image(image)
    try:
        new_plant=PlantModel(nursery_id=nursery.nursery_id,name=name,description=description,price=price,stock=stock,image_url=image_url)
        db.add(new_plant)
        db.commit()
        db.refresh(new_plant)
        print(new_plant)
        return {"message":"Plant Added Successfully"}
    except Exception as e:
           db.rollback()
           image_path = Path(f".{image_url}")
           image_path = Path(f".{image_url}")
           if image_path.exists():
                image_path.unlink()
           raise HTTPException(status_code=400, detail=str(e))
async def save_image(image: UploadFile) -> str:
    if not image:
        raise HTTPException(status_code=400, detail="Image is required")
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(image.filename)[1]
    filename = f"{timestamp}{file_extension}"
    file_path = UPLOAD_DIR / filename
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to save image: {str(e)}")
    return f"/static/plant_images/{filename}"
    
async def validate_image(image: UploadFile) -> None:
    if not image:
        raise HTTPException(status_code=400, detail="Image is required")
    
    image.file.seek(0, 2)  # Seek to end of file
    size = image.file.tell()
    image.file.seek(0)  # Reset file pointer

    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
    file_extension = os.path.splitext(image.filename)[1].lower()
    
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Only {', '.join(ALLOWED_EXTENSIONS)} files are allowed"
        )    