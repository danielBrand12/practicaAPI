from tortoise import fields, Tortoise
from tortoise.models import Model
from passlib.hash import bcrypt


class customer(Model):
    custid = fields.IntField(pk=True)
    firstname = fields.CharField(max_length=30)
    lastname = fields.CharField(max_length=50)
    address = fields.CharField(max_length=100)
    city = fields.CharField(max_length=100)
    email = fields.CharField(max_length=60)
    password = fields.CharField(max_length=60)

    def verify_password(self, password):
        return True if self.password == password else False

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


Tortoise.init_models(["app.models.models"], "models")