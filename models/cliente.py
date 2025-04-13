from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False,)
    agencia = db.Column(db.String(10), nullable=False)
    conta = db.Column(db.String(20), nullable=False)
    saldo = db.Column(db.Numeric(10,2), nullable=False)
    nivel = db.Column(db.String(20), nullable=False)
    produtos = db.Column(db.String(200), nullable=True)