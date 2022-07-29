from fastapi import APIRouter, HTTPException
from app.models.models import plant
from app.schemas.schemas import plant_pydantic, plantIn_pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError
from typing import List
from pydantic import BaseModel

router = APIRouter(
    prefix="/plant",
    tags=["Plants"],
    responses={404: {"description": "Not found"}}
)


class Status(BaseModel):
    message: str

@router.get(
    '',
    response_model=List[plant_pydantic]
)
async def get_plants():
    return await plant_pydantic.from_queryset(plant.all())


@router.get(
    '/{id}',
    response_model=plant_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_plant(id: int):
    return await plant_pydantic.from_queryset_single(plant.get(id=id))


@router.post(
    '',
    response_model=plant_pydantic
)
async def create_plant(plt: plant_pydantic):
    plant_creado = await plant.create(**plt.dict(exclude_unset=True))
    return await plant_creado.from_tortoise_orm(plant_creado)


@router.put(
    '/{id}',
    response_model=plant_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_plant(id: int, plt: plantIn_pydantic):
    await plant.filter(id=id).update(**plt.dict())
    return await plant_pydantic.from_queryset_single(plant.get(id=id))


@router.delete(
    '/{id}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_plant(id: int):
    deleted_plant = await plant.filter(id=id).delete()
    if not deleted_plant:
        raise HTTPException(status_code=404, detail=f"Plant {id} not found")
    return Status(message=f"Deleted plant {id}")