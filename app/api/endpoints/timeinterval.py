from fastapi import APIRouter, HTTPException
from app.models.models import timeinterval
from app.schemas.schemas import timeinterval_pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError
from typing import List
from pydantic import BaseModel


class Status(BaseModel):
    message: str


router = APIRouter(
    prefix="/time-interval",
    tags=["Time Intervals"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    '',
    response_model=List[timeinterval_pydantic]
)
async def get_timeintervals():
    return await timeinterval_pydantic.from_queryset(timeinterval.all())


@router.get(
    '/{id}',
    response_model=timeinterval_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_timeinterval_by_id(timeid: int):
    return await timeinterval_pydantic.from_queryset_single(timeinterval.get(timeid=timeid))


@router.post(
    '',
    response_model=timeinterval_pydantic
)
async def create_timeinterval(time: timeinterval_pydantic):
    created_timeinterval = await timeinterval.create(**time.dict())
    return await timeinterval_pydantic.from_tortoise_orm(created_timeinterval)

@router.delete(
    '/{id}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_timeinterval(timeid: int):
    deleted_timeinterval = await timeinterval.filter(timeid=timeid).delete()
    if not deleted_timeinterval:
        raise HTTPException(status_code=404, detail=f"Timeinterval {timeid} not found")
    return Status(message=f"Deleted timeinterval {timeid}")