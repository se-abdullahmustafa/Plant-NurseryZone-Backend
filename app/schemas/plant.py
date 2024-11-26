from pydantic import BaseModel, ConfigDict,constr,StringConstraints
from typing import Optional,Annotated

class PlantCreate(BaseModel):
    nursery_id:int
    name:Annotated[str, StringConstraints(max_length=200)]
    description:str
    price:str
    stock:Optional[int]=0
    image_url:str
    
class PlantResponse(BaseModel):
    nursery_id:int
    plant_id:int
    name:str
    description:str
    price:str
    stock:int
    image_url:str
    model_config = ConfigDict(from_attributes=True)
