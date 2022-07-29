from tortoise import fields, Tortoise
from tortoise.models import Model
from stock import stock
from lineitem import lineitem


class demand(Model):
    id = fields.IntField(pk=True)
    stockid: fields.ForeignKeyRelation[stock] = fields.ForeignKeyField('models.stock', related_name='stock')
    lineitemid: fields.ForeignKeyRelation[lineitem] = fields.ForeignKeyField('models.lineitem', related_name='line item')