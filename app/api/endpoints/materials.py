from fastapi import APIRouter, HTTPException
from app.models.models import material
from app.schemas.schemas import material_pydantic, materialIn_pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError
from typing import List
from pydantic import BaseModel

router = APIRouter(
    prefix="/materials",
    tags=["Materials"],
    responses={404: {"description": "Not found"}},
)


class Status(BaseModel):
    message: str


@router.get(
    '',
    response_model=List[material_pydantic]
)
async def get_materials():
    return await material_pydantic.from_queryset(material.all())


@router.get(
    '/{id}',
    response_model=material_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_material(id: int):
    return await material_pydantic.from_queryset_single(material.get(id=id))


@router.post(
    '',
    response_model=material_pydantic
)
async def create_material(mat: material_pydantic):
    material_creado = await material.create(**mat.dict(exclude_unset=True))
    return await material_pydantic.from_tortoise_orm(material_creado)


@router.put(
    '/{id}',
    response_model=material_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_material(id: int, mat: materialIn_pydantic):
    await material.filter(id=id).update(**mat.dict())
    return await material_pydantic.from_queryset_single(material.get(id=id))


@router.delete(
    '/{id}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_material(id: int):
    deleted_material = await material.filter(id=id).delete()
    if not deleted_material:
        raise HTTPException(status_code=404, detail=f"Material {id} not found")
    return Status(message=f"Deleted material {id}")