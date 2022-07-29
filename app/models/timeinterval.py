from tortoise import fields
from tortoise.models import Model


class timeinterval(Model):
    timeid = fields.IntField(pk=True)
    initialdate = fields.DateField()
    finaldate = fields.DateField()

    def __str__(self):
        return str(self.initialdate) + " " + str(self.finaldate)

    class PydanticMeta:
        computed = ["__str__"]
        exclude = ["interval"]