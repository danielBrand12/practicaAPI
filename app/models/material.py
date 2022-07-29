from tortoise import fields
from tortoise.models import Model


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