import uvicorn
from fastapi import FastAPI
from app.api.api import api_router
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()
app.include_router(api_router)



register_tortoise(
    app,
    #db_url="postgres://postgres:davidb007@localhost:5432/Stock Management",
    db_url="postgres://postgres:postgres@db:5432/stock_management",
    modules={"models": ["app.models.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == '__main__':
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000)
