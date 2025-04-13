from models.cliente import db
from datetime import datetime

class Investimento(db.Model):
    __tablename__ = 'investimentos'
    
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # "acao" ou "moeda"
    simbolo = db.Column(db.String(20), nullable=False)  # Código da ação ou moeda
    quantidade = db.Column(db.Float, nullable=False)
    preco_compra = db.Column(db.Float, nullable=False)
    data_compra = db.Column(db.DateTime, default=datetime.utcnow)