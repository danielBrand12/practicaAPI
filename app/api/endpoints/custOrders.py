from fastapi import APIRouter, HTTPException
from app.models.models import cust_order2
from app.schemas.schemas import cust_order2_pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError
from typing import List
from pydantic import BaseModel

router = APIRouter(
    prefix="/cust-orders",
    tags=["Customer Orders"],
    responses={404: {"description": "Not found"}},
)


class Status(BaseModel):
    message: str


@router.get(
    '',
    response_model=List[cust_order2_pydantic]
)
async def show_orders():
    return await cust_order2_pydantic.from_queryset(cust_order2.all())


@router.get(
    '/{id}',
    response_model=cust_order2_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_cust_order_by_id(id: int):
    return await cust_order2_pydantic.from_queryset_single(cust_order2.get(id=id))


@router.post(
    '',
    response_model=cust_order2_pydantic
)
async def create_cust_order(custid: int, timeid: int):
    created_cust_order = await cust_order2.create(customerid_id=custid, intervalid_id=timeid)
    return await cust_order2_pydantic.from_tortoise_orm(created_cust_order)


@router.delete(
    '/{id}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_cust_order(id: int):
    deleted_cust_order = await cust_order2.filter(id=id).delete()
    if not deleted_cust_order:
        raise HTTPException(status_code=404, detail=f"Customer order {id} not found")
    return Status(message=f"Deleted customer order {id}")