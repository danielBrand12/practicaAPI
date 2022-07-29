from app.schemas import token
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.models.models import customer
from app.schemas.schemas import customer_pydantic
from typing import Union, List
from pydantic import BaseModel


SECRET_KEY = "0692f16229b8d097cafbaa339237751164213c70b2c1f500a2198119bb25777a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token",
                                     scopes={"me": "Read information about the current user."},)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[int, None] = None
    scopes: List[str] = []


async def authenticate_customer(id: int, password: str):
    cust = await customer.get(custid=id)
    if not customer:
        return False
    if not cust.verify_password(password):
        return False
    return cust


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_customer(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        cust = await customer.get(custid=payload.get('custid'))
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=payload.get('custid'))
    except JWTError:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return await customer_pydantic.from_tortoise_orm(cust)