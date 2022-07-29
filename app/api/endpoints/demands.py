from fastapi import APIRouter, HTTPException
from app.models.models import demand
from app.schemas.schemas import demand_pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError
from typing import List
from pydantic import BaseModel

router = APIRouter(
    prefix="/demands",
    tags=["Demands"],
    responses={404: {"description": "Not found"}},
)


class Status(BaseModel):
    message: str


@router.get(
    '',
    response_model=List[demand_pydantic]
)
async def show_demands():
    return await demand_pydantic.from_queryset(demand.all())


@router.get(
    '/{id}',
    response_model=demand_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_demand_by_id(id: int):
    return await demand_pydantic.from_queryset_single(demand.get(id=id))


@router.post(
    '',
    response_model=demand_pydantic
)
async def create_demand(stockid: int, lineitemid: int):
    created_demand = await demand.create(stockid=stockid, lineitemid=lineitemid)
    return await demand_pydantic.from_tortoise_orm(created_demand)


@router.delete(
    '/{id}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_demand(id: int):
    deleted_demand = await demand.filter(id=id).delete()
    if not deleted_demand:
        raise HTTPException(status_code=404, detail=f"Demand {id} not found")
    return Status(message=f"Deleted demand {id}")