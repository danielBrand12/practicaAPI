from tortoise import fields, Tortoise
from tortoise.models import Model
from plant import plant


class storagelocation(Model):
    id = fields.IntField(pk=True)
    address = fields.CharField(max_length=50)
    type = fields.CharField(max_length=50)
    plantid: fields.ForeignKeyRelation[plant] = fields.ForeignKeyField('models.plant', related_name="plant")
    area = fields.FloatField()

    class PydanticMeta:
        computed = ["__str__"]
        exclude = ["storage location"]