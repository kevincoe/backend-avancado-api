from flask_marshmallow import Marshmallow
from models.cliente import Cliente
from marshmallow import fields

ma = Marshmallow()

class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        include_fk = True
        
    id = ma.Integer(dump_only=True)
    nome = ma.String(required=True)
    agencia = ma.String(required=True)
    conta = ma.String(required=True)
    saldo = fields.Decimal(places=2, as_string=True, required=True)
    nivel = ma.String(required=True)
    produtos = ma.String(required=False)