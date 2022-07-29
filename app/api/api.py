from fastapi import APIRouter

from app.api.endpoints import plant, lineitem, timeinterval, custOrders, storageLocations
from app.api.endpoints import customers, demands, materials, login

api_router = APIRouter()
api_router.include_router(customers.router)
api_router.include_router(plant.router)
api_router.include_router(lineitem.router)
api_router.include_router(timeinterval.router)
api_router.include_router(demands.router)
api_router.include_router(materials.router)
api_router.include_router(custOrders.router)
api_router.include_router(storageLocations.router)
api_router.include_router((login.router))