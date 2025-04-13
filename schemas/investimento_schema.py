from flask_marshmallow import Marshmallow
from models.investimento import Investimento

ma = Marshmallow()

class InvestimentoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Investimento
        include_fk = True
    
    id = ma.Integer(dump_only=True)
    cliente_id = ma.Integer(required=True)
    tipo = ma.String(required=True)
    simbolo = ma.String(required=True)
    quantidade = ma.Float(required=True)
    preco_compra = ma.Float(dump_only=True)
    data_compra = ma.DateTime(dump_only=True)