from tortoise import fields, Tortoise
from tortoise.models import Model
from storagelocation import storagelocation
from material import material


class stock(Model):
    # id = fields.IntField()
    storagelocationid: fields.ForeignKeyRelation[storagelocation] = fields.ForeignKeyField('models.storagelocation', related_name="storage location")
    materialid: fields.ForeignKeyRelation[material] = fields.ForeignKeyField('models.material', related_name="material")

    class PydanticMeta:
        computed = ["__str__"]
        exclude = ["stock"]
