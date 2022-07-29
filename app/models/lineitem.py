from tortoise import fields, Tortoise
from tortoise.models import Model
from cust_order import cust_order
from material import material

class lineitem(Model):
    id = fields.IntField(pk=True)
    orderid: fields.ForeignKeyRelation[cust_order] = fields.ForeignKeyField('models.cust_order2', related_name="order")
    materialid: fields.ForeignKeyRelation[material] = fields.ForeignKeyField('models.material', related_name="mat")

    class PydanticMeta:
        computed = ["__str__"]
        exclude = ["line item"]
