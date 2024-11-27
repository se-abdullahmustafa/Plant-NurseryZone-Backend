from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id:int
    plant_id:int
    quntity:int
class OrderResponse(BaseModel):
    user_id:int
    plant_id:int
    order_id:int
    quantity:int
    total_amount:float
    status:str  
    created_at:str
   