import tortoise.exceptions
from tortoise import Tortoise, run_async, fields
from tortoise.models import Model
import datetime

class customer(Model):
    custid = fields.IntField(pk=True)
    firstname = fields.CharField(max_length=30)
    lastname = fields.CharField(max_length=50)
    address = fields.CharField(max_length=100)
    city = fields.CharField(max_length=100)

    def __str__(self):
        return self.firstname

class cust_order2(Model):
    customerid = fields.ForeignKeyField('models.customer')
    intervalid = fields.ForeignKeyField('models.timeinterval')

class timeinterval(Model):
    timeid = fields.IntField(pk=True)
    initialdate = fields.DateField()
    finaldate = fields.DateField()

    def __str__(self):
        return str(self.initialdate) + " " + str(self.finaldate)



async def run():
    await Tortoise.init(
        {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "host": "localhost",
                        "port": "5432",
                        "user": "postgres",
                        "password": "davidb007",
                        "database": "Stock Management",
                    },
                }
            },
            "apps": {"models": {"models": ["__main__"], "default_connection": "default"}},
        },
        #_create_db=True,
    )
    await Tortoise.generate_schemas()

    print(await customer.all().distinct())

    async for cust in customer.all():
        print(cust.firstname, cust.lastname)

    print("")

    query = await customer.filter(custid__in=[123, 1236, 5])
    print(query)
    for cust in query:
        print(cust.firstname, cust.lastname)

    async for cust in cust_order2.all():
        print(cust.customerid.pk, cust.customerid.firstname)

    """ 

    customers = await customer.filter(custid=1236).first()
    interval = await timeinterval.filter(timeid=1).first()
    #print(type(customers))

    await cust_order2.create(customerid=customers, intervalid=interval)
"""

    initialdate = datetime.date(2022, 7, 21)
    finaldate = datetime.date(2022, 7, 28)
    event = await timeinterval.create(timeid=5, initialdate=initialdate, finaldate=finaldate)
    print(type(event))


    custid = 5
    firstname = "Juan"
    lastname = "Cuadrado"
    address = "Sincelejo"
    city = "Medellín"
    print(await customer.create(custid=custid,
                                firstname=firstname,
                                lastname=lastname,
                                address=address,
                                city=city))

    #print(await modelos.customer.filter(firstname=firstname,lastname=lastname,address=address,city=city).first())
    #await Tortoise._drop_databases()


if __name__ == "__main__":
    run_async(run())

"""
import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from models import customer_pydantic, customerIn_pydantic, customer, \
    timeinterval_pydantic, timeinterval, \
    cust_order2_pydantic, cust_order2, \
    material, material_pydantic, materialIn_pydantic,\
    lineitem_pydantic, lineitem, \
    plant_pydantic, plantIn_pydantic, plant, \
    storagelocation_pydantic, storagelocationIn_pydantic, storagelocation, \
    demand_pydantic, demand

router = FastAPI(title="Tortoise ORM FastAPI example")


register_tortoise(
    router,
    db_url="postgres://postgres:davidb007@localhost:5432/Stock Management",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


class Status(BaseModel):
    message: str

class CustOrder(BaseModel):
    id: int
    customerid_id: int
    intervalid_id: int

    class Config:
        orm_mode = True


@router.get(
    '/customer',
    response_model=List[customer_pydantic]
)
async def get_customers():
    return await customer_pydantic.from_queryset(customer.all())


@router.get(
    '/customer/{custid}',
    response_model=customer_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_customer(custid: int):
    return await customer_pydantic.from_queryset_single(customer.get(custid=custid))


@router.get(
    '/filter/customer',
    response_model=List[customer_pydantic],
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_customers_by_name(firstname: str):
    return await customer_pydantic.from_queryset(customer.filter(firstname=firstname))


@router.post(
    '/customer',
    response_model=customer_pydantic
)
async def create_customer(cust: customer_pydantic):
    customer_creado = await customer.create(**cust.dict(exclude_unset=True)) #Exclude unset excluye los campos que no se pasan como parámetro
    return await customer_pydantic.from_tortoise_orm(customer_creado)


@router.put(                                           #Petición para modificar un dato
    '/customer/{custid}',
    response_model=customer_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_customer(custid: int, cust: customerIn_pydantic):
    await customer.filter(custid=custid).update(**cust.dict())
    return await customer_pydantic.from_queryset_single(customer.get(custid=custid))


@router.delete(
    '/customer/{custid}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_customer(custid: int):
    deleted_customer = await customer.filter(custid=custid).delete()
    if not deleted_customer:
        raise HTTPException(status_code=404, detail=f"Customer {custid} not found")
    return Status(message=f"Deleted customer {custid}")


@router.get(
    '/timeinterval',
    response_model=List[timeinterval_pydantic]
)
async def get_timeintervals():
    return await timeinterval_pydantic.from_queryset(timeinterval.all())


@router.get(
    '/timeinterval/{timeid}',
    response_model=timeinterval_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_timeinterval_by_id(timeid: int):
    return await timeinterval_pydantic.from_queryset_single(timeinterval.get(timeid=timeid))


@router.post(
    '/timeinterval',
    response_model=timeinterval_pydantic
)
async def create_timeinterval(time: timeinterval_pydantic):
    created_timeinterval = await timeinterval.create(**time.dict())
    return await timeinterval_pydantic.from_tortoise_orm(created_timeinterval)

@router.delete(
    '/timeinterval/{timeid}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_timeinterval(timeid: int):
    deleted_timeinterval = await timeinterval.filter(timeid=timeid).delete()
    if not deleted_timeinterval:
        raise HTTPException(status_code=404, detail=f"Timeinterval {timeid} not found")
    return Status(message=f"Deleted timeinterval {timeid}")


@router.get(
    '/cust-order',
    response_model=List[cust_order2_pydantic]
)
async def show_orders():
    return await cust_order2_pydantic.from_queryset(cust_order2.all())


@router.get(
    '/cust-order/{id}',
    response_model=cust_order2_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_cust_order_by_id(id: int):
    return await cust_order2_pydantic.from_queryset_single(cust_order2.get(id=id))


@router.post(
    '/cust-order/',
    response_model=cust_order2_pydantic
)
async def create_cust_order(custid: int, timeid: int):
    created_cust_order = await cust_order2.create(customerid_id=custid, intervalid_id=timeid)
    return await cust_order2_pydantic.from_tortoise_orm(created_cust_order)


@router.delete(
    '/cust-order/{id}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_cust_order(id: int):
    deleted_cust_order = await cust_order2.filter(id=id).delete()
    if not deleted_cust_order:
        raise HTTPException(status_code=404, detail=f"Customer order {id} not found")
    return Status(message=f"Deleted customer order {id}")


@router.get(
    '/material',
    response_model=List[material_pydantic]
)
async def get_materials():
    return await material_pydantic.from_queryset(material.all())


@router.get(
    '/material/{id}',
    response_model=material_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_material(id: int):
    return await material_pydantic.from_queryset_single(material.get(id=id))


@router.post(
    '/material',
    response_model=material_pydantic
)
async def create_material(mat: material_pydantic):
    material_creado = await material.create(**mat.dict(exclude_unset=True))
    return await material_pydantic.from_tortoise_orm(material_creado)


@router.put(
    '/material/{id}',
    response_model=material_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_material(id: int, mat: materialIn_pydantic):
    await material.filter(id=id).update(**mat.dict())
    return await material_pydantic.from_queryset_single(material.get(id=id))


@router.delete(
    '/material/{id}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_material(id: int):
    deleted_material = await material.filter(id=id).delete()
    if not deleted_material:
        raise HTTPException(status_code=404, detail=f"Material {id} not found")
    return Status(message=f"Deleted material {id}")


@router.get(
    '/lineitem',
    response_model=List[lineitem_pydantic]
)
async def show_lineitems():
    return await lineitem_pydantic.from_queryset(lineitem.all())


@router.get(
    '/lineitem/{id}',
    response_model=lineitem_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_lineitem_by_id(id: int):
    return await lineitem_pydantic.from_queryset_single(lineitem.get(id=id))


@router.post(
    '/lineitem/',
    response_model=lineitem_pydantic
)
async def create_lineitem(orderid: int, materialid: int):
    created_lineitem = await lineitem.create(orderid=orderid, materialid=materialid)
    return await lineitem_pydantic.from_tortoise_orm(created_lineitem)


@router.delete(
    '/lineitem/{id}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_lineitem(id: int):
    deleted_linitem= await lineitem.filter(id=id).delete()
    if not deleted_linitem:
        raise HTTPException(status_code=404, detail=f"Line item {id} not found")
    return Status(message=f"Deleted line item {id}")


@router.get(
    '/plant',
    response_model=List[plant_pydantic]
)
async def get_plants():
    return await plant_pydantic.from_queryset(plant.all())


@router.get(
    '/plant/{id}',
    response_model=plant_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_plant(id: int):
    return await plant_pydantic.from_queryset_single(plant.get(id=id))


@router.post(
    '/plant',
    response_model=plant_pydantic
)
async def create_plant(plt: plant_pydantic):
    plant_creado = await plant.create(**plt.dict(exclude_unset=True))
    return await plant_creado.from_tortoise_orm(plant_creado)


@router.put(
    '/plant/{id}',
    response_model=plant_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_plant(id: int, plt: plantIn_pydantic):
    await plant.filter(id=id).update(**plt.dict())
    return await plant_pydantic.from_queryset_single(plant.get(id=id))


@router.delete(
    '/plant/{id}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_plant(id: int):
    deleted_plant = await plant.filter(id=id).delete()
    if not deleted_plant:
        raise HTTPException(status_code=404, detail=f"Plant {id} not found")
    return Status(message=f"Deleted plant {id}")


@router.get(
    '/storage-location',
    response_model=List[storagelocation_pydantic]
)
async def get_storage_locations():
    return await storagelocation_pydantic.from_queryset(storagelocation.all())


@router.get(
    '/storage-location/{id}',
    response_model=storagelocation_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_storage_location(id: int):
    return await storagelocation_pydantic.from_queryset_single(storagelocation.get(id=id))


@router.post(
    '/storage-location',
    response_model=storagelocation_pydantic
)
async def create_plant(sl: storagelocation_pydantic):
    sl_creado = await plant.create(**sl.dict(exclude_unset=True))
    return await storagelocation_pydantic.from_tortoise_orm(sl_creado)


@router.put(
    '/storage-location/{id}',
    response_model=storagelocation_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_plant(id: int, sl: storagelocationIn_pydantic):
    await storagelocation.filter(id=id).update(**sl.dict())
    return await storagelocation_pydantic.from_queryset_single(storagelocation.get(id=id))


@router.delete(
    '/storage-location/{id}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_plant(id: int):
    deleted_sl = await storagelocation.filter(id=id).delete()
    if not deleted_sl:
        raise HTTPException(status_code=404, detail=f"Storage locaiton {id} not found")
    return Status(message=f"Deleted storage location {id}")


@router.get(
    '/demand',
    response_model=List[demand_pydantic]
)
async def show_demands():
    return await demand_pydantic.from_queryset(demand.all())


@router.get(
    '/demand/{id}',
    response_model=demand_pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_demand_by_id(id: int):
    return await demand_pydantic.from_queryset_single(demand.get(id=id))


@router.post(
    '/demand/',
    response_model=demand_pydantic
)
async def create_demand(stockid: int, lineitemid: int):
    created_demand = await lineitem.create(stockid=stockid, lineitemid=lineitemid)
    return await demand_pydantic.from_tortoise_orm(created_demand)


@router.delete(
    '/demand/{id}',
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_demand(id: int):
    deleted_demand = await demand.filter(id=id).delete()
    if not deleted_demand:
        raise HTTPException(status_code=404, detail=f"Demand {id} not found")
    return Status(message=f"Deleted demand {id}")


if __name__ == "__main__":
    uvicorn.run(router, host='0.0.0.0', port=8000)
"""

"""
from tortoise import fields, Tortoise
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class customer(Model):
    custid = fields.IntField(pk=True)
    firstname = fields.CharField(max_length=30)
    lastname = fields.CharField(max_length=50)
    address = fields.CharField(max_length=100)
    city = fields.CharField(max_length=100)

    def __str__(self):
        return self.firstname

    class PydanticMeta:
        computed = ["__str__"]
        exclude = ["customer"]


class timeinterval(Model):
    timeid = fields.IntField(pk=True)
    initialdate = fields.DateField()
    finaldate = fields.DateField()

    def __str__(self):
        return str(self.initialdate) + " " + str(self.finaldate)

    class PydanticMeta:
        computed = ["__str__"]
        exclude = ["interval"]


class cust_order2(Model):
    customerid: fields.ForeignKeyRelation[customer] = fields.ForeignKeyField('models.customer', related_name='customer')
    intervalid: fields.ForeignKeyRelation[timeinterval] = fields.ForeignKeyField('models.timeinterval', related_name='interval')

    class PydanticMeta:
        computed = ["__str__"]
        exclude = ["order"]


class material(Model):
    id = fields.IntField(pk=True)
    type = fields.CharField(max_length=50)
    name = fields.CharField(max_length=100)
    price = fields.FloatField()

    def __str__(self):
        return str(self.name)

    class PydanticMeta:
        computed = ["__str__"]
        exclude = ["mat", "material"]


class lineitem(Model):
    id = fields.IntField(pk=True)
    orderid: fields.ForeignKeyRelation[cust_order2] = fields.ForeignKeyField('models.cust_order2', related_name="order")
    materialid: fields.ForeignKeyRelation[material] = fields.ForeignKeyField('models.material', related_name="mat")

    class PydanticMeta:
        computed = ["__str__"]
        exclude = ["line item"]


class plant(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    city = fields.CharField(max_length=50)
    address = fields.CharField(max_length=50)

    class PydanticMeta:
        computed = ["__str__"]
        exclude = ["plant"]


class storagelocation(Model):
    id = fields.IntField(pk=True)
    address = fields.CharField(max_length=50)
    type = fields.CharField(max_length=50)
    plantid: fields.ForeignKeyRelation[plant] = fields.ForeignKeyField('models.plant', related_name="plant")
    area = fields.FloatField()

    class PydanticMeta:
        computed = ["__str__"]
        exclude = ["storage location"]


class stock(Model):
    # id = fields.IntField()
    storagelocationid: fields.ForeignKeyRelation[storagelocation] = fields.ForeignKeyField('models.storagelocation', related_name="storage location")
    materialid: fields.ForeignKeyRelation[material] = fields.ForeignKeyField('models.material', related_name="material")

    class PydanticMeta:
        computed = ["__str__"]
        exclude = ["stock"]


class demand(Model):
    id = fields.IntField(pk=True)
    stockid: fields.ForeignKeyRelation[stock] = fields.ForeignKeyField('models.stock', related_name='stock')
    lineitemid: fields.ForeignKeyRelation[lineitem] = fields.ForeignKeyField('models.lineitem', related_name='line item')

Tortoise.init_models(["models"], "models")

customer_pydantic = pydantic_model_creator(customer, name="Customer")
customerIn_pydantic = pydantic_model_creator(customer, name="CustomerIn", exclude_readonly=True)
cust_order2_pydantic = pydantic_model_creator(cust_order2, name="Cust_Order")
timeinterval_pydantic = pydantic_model_creator(timeinterval, name="Time_Interval")
material_pydantic = pydantic_model_creator(material, name="Material")
materialIn_pydantic = pydantic_model_creator(material, name="MaterialIn", exclude_readonly=True)
lineitem_pydantic = pydantic_model_creator(lineitem, name="Line_Item")
plant_pydantic = pydantic_model_creator(plant, name="Plant")
plantIn_pydantic = pydantic_model_creator(plant, name="PlantIn", exclude_readonly=True)
storagelocation_pydantic = pydantic_model_creator(storagelocation, name="Storage_Location")
storagelocationIn_pydantic = pydantic_model_creator(storagelocation, name="Storage_LocationIn", exclude_readonly=True)
stock_pydantic = pydantic_model_creator(stock, name="Stock")
demand_pydantic = pydantic_model_creator(demand, name="Demand")

"""