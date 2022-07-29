from tortoise import fields, Tortoise
from tortoise.models import Model


class plant(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    city = fields.CharField(max_length=50)
    address = fields.CharField(max_length=50)

    class PydanticMeta:
        computed = ["__str__"]
        exclude = ["plant"]
