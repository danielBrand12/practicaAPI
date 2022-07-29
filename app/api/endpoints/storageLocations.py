from fastapi import APIRouter, HTTPException
from app.models.models import storagelocation
from app.schemas.schemas import storagelocation_pydantic, storagelocationIn_pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError
from typing import List
from pydantic import BaseModel

router = APIRouter(
    prefix="/storage-locations",
    tags=["Storage Locations"],
    responses={404: {"description": "Not found"}},
)


class Status(BaseModel):
    message: str


@router.get(
    '',
    response_model=List[storagelocation_pydantic]
)
async def get_storage_locations():
    return await storagelocation_pydantic.from_queryset(storagelocation.all())


@router.get(
    '/{id}',
    response_model=storagelocation_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_storage_location(id: int):
    return await storagelocation_pydantic.from_queryset_single(storagelocation.get(id=id))


@router.post(
    '',
    response_model=storagelocation_pydantic
)
async def create_storage_location(sl: storagelocation_pydantic):
    sl_creado = await storagelocation.create(**sl.dict(exclude_unset=True))
    return await storagelocation_pydantic.from_tortoise_orm(sl_creado)


@router.put(
    '/{id}',
    response_model=storagelocation_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_storage_location(id: int, sl: storagelocationIn_pydantic):
    await storagelocation.filter(id=id).update(**sl.dict())
    return await storagelocation_pydantic.from_queryset_single(storagelocation.get(id=id))


@router.delete(
    '/{id}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_storage_location(id: int):
    deleted_sl = await storagelocation.filter(id=id).delete()
    if not deleted_sl:
        raise HTTPException(status_code=404, detail=f"Storage location {id} not found")
    return Status(message=f"Deleted storage location {id}")