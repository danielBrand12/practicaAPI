from tortoise import fields, Tortoise
from tortoise.models import Model


class customer(Model):
    id = fields.IntField(pk=True)
    firstname = fields.CharField(max_length=30)
    lastname = fields.CharField(max_length=50)
    address = fields.CharField(max_length=100)
    city = fields.CharField(max_length=100)

    def __str__(self):
        return self.firstname

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    class PydanticMeta:
        computed = ["__str__"]
        exclude = ["customer"]


Tortoise.init_models(["app.models.customer"], "models")