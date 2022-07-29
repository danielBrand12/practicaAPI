from fastapi import APIRouter, HTTPException, Depends, status, Security, Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from app.models.models import customer
from app.schemas.schemas import customer_pydantic, customerIn_pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError
from typing import List
from pydantic import BaseModel
from typing import Union
from app.api.endpoints.login import authenticate_customer, get_current_customer, create_access_token, Token

from app.core.celery_app import create_task


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


router = APIRouter(
    tags=["Customers"],
    responses={404: {"description": "Not found"}},
)


class Status(BaseModel):
    message: str


@router.post("/token", response_model=Token)
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_customer(int(form_data.username), form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )

    user_obj = await customer_pydantic.from_tortoise_orm(user)
    dict_user_obj = user_obj.dict()
    dict_user_obj["scopes"] = form_data.scopes
    token = create_access_token(dict_user_obj)

    return {'access_token': token, 'token_type': 'bearer'}


@router.get("/customers/me", response_model=customer_pydantic)
async def get_session_customer(cust: customer_pydantic = Security(get_current_customer, scopes=["me"])):
    return cust


@router.get(
    '/customers',
    response_model=List[customer_pydantic]
)
async def get_customers():
    #celery_app.send_task('test.celery', args=['Hola!'])
    return await customer_pydantic.from_queryset(customer.all())


@router.get(
    '/customers/{id}',
    response_model=customer_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_customer(custid: int):
    return await customer_pydantic.from_queryset_single(customer.get(custid=custid))


@router.get(
    '/customers/filter',
    response_model=List[customer_pydantic],
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_customers_by_name(firstname: str):
    return await customer_pydantic.from_queryset(customer.filter(firstname=firstname))


@router.post(
    '/customers',
    response_model=customer_pydantic
)
async def create_customer(cust: customer_pydantic):
    customer_creado = await customer.create(**cust.dict(exclude_unset=True)) #Exclude unset excluye los campos que no se pasan como parámetro
    return await customer_pydantic.from_tortoise_orm(customer_creado)


@router.put(                                           #Petición para modificar un dato
    '/customers/{id}',
    response_model=customer_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_customer(custid: int, cust: customerIn_pydantic):
    await customer.filter(custid=custid).update(**cust.dict())
    return await customer_pydantic.from_queryset_single(customer.get(custid=custid))


@router.delete(
    '/customers/{id}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_customer(custid: int):
    deleted_customer = await customer.filter(custid=custid).delete()
    if not deleted_customer:
        raise HTTPException(status_code=404, detail=f"Customer {custid} not found")
    return Status(message=f"Deleted customer {custid}")



@router.post("/tasks", status_code=201)
def run_task(payload=Body(...)):
    #task_type = payload["type"]
    task = create_task.delay(5)
    return JSONResponse({"task_id": task.id})