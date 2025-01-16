from fastapi import FastAPI
from pathlib import Path
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.routers import user_route,nursery_route,order_route,feedback_route,delivery_route
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Nursery Plant Zone",description="Online Plateform to sell plants.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

app.include_router(router=user_route.router, prefix="/api", tags=["User"])
app.include_router(router=nursery_route.router, prefix="/api", tags=["Nursery"])
app.include_router(router=order_route.router,prefix="/api",tags=["Order"])
app.include_router(router=feedback_route.router,prefix="/api",tags=["Feedback"])
app.include_router(router=delivery_route.router,prefix="/api",tags=["DeliveryBoy"])

app.mount("/api/static/plant_images", StaticFiles(directory="static/plant_images"), name="plant_images")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")