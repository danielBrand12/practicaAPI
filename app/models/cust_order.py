from tortoise import fields, Tortoise
from tortoise.models import Model
from customer import customer
from timeinterval import timeinterval


class cust_order(Model):
    customerid: fields.ForeignKeyRelation[customer] = fields.ForeignKeyField('customer.customer', related_name='customer')
    intervalid: fields.ForeignKeyRelation[timeinterval] = fields.ForeignKeyField('timeinterval.timeinterval', related_name='interval')

    class PydanticMeta:
        computed = ["__str__"]
        exclude = ["order"]

Tortoise.init_models(["app.models.cust_order"], "models")