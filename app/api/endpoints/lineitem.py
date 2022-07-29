from fastapi import APIRouter, HTTPException
from app.models.models import lineitem
from app.schemas.schemas import lineitem_pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError
from typing import List
from pydantic import BaseModel

router = APIRouter(
    prefix="/lineitems",
    tags=["Line Items"],
    responses={404: {"description": "Not found"}},
)


class Status(BaseModel):
    message: str


@router.get(
    '',
    response_model=List[lineitem_pydantic]
)
async def show_lineitems():
    return await lineitem_pydantic.from_queryset(lineitem.all())


@router.get(
    '/{id}',
    response_model=lineitem_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_lineitem_by_id(id: int):
    return await lineitem_pydantic.from_queryset_single(lineitem.get(id=id))


@router.post(
    '/',
    response_model=lineitem_pydantic
)
async def create_lineitem(orderid: int, materialid: int):
    created_lineitem = await lineitem.create(orderid=orderid, materialid=materialid)
    return await lineitem_pydantic.from_tortoise_orm(created_lineitem)


@router.delete(
    '/{id}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_lineitem(id: int):
    deleted_linitem= await lineitem.filter(id=id).delete()
    if not deleted_linitem:
        raise HTTPException(status_code=404, detail=f"Line item {id} not found")
    return Status(message=f"Deleted line item {id}")