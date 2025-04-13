from models.cliente import db, Cliente
from decimal import Decimal

class ClienteController:
    @staticmethod
    def listar_clientes():
        return Cliente.query.all()

    @staticmethod
    def obter_cliente(id):
        return Cliente.query.get_or_404(id)

    @staticmethod
    def criar_cliente(data):
        try:
            novo_cliente = Cliente(
                nome=data['nome'],
                agencia=data['agencia'],
                conta=data['conta'],
                nivel=data['nivel'],
                saldo=round(float(data.get('saldo', 0.0)), 2),
                produtos=data.get('produtos', '')
            )
            db.session.add(novo_cliente)
            db.session.commit()
            return novo_cliente
        except Exception as e:
            db.session.rollback()
            return {"erro": f"Erro ao criar cliente: {str(e)}"}, 500

    @staticmethod
    def atualizar_cliente(id, data):
        try:
            cliente = Cliente.query.get_or_404(id)
            if 'nome' in data:
                cliente.nome = data['nome']
            if 'agencia' in data:
                cliente.agencia = data['agencia']
            if 'conta' in data:
                cliente.conta = data['conta']
            if 'nivel' in data:
                cliente.nivel = data['nivel']
            if 'produtos' in data:
                cliente.produtos = data['produtos']
            if 'saldo' in data:
                cliente.saldo = Decimal(str(data['saldo']))
            db.session.commit()
            return cliente
        except Exception as e:
            db.session.rollback()
            return {"erro": f"Erro ao atualizar cliente: {str(e)}"}, 500

    @staticmethod
    def remover_cliente(id):
        try:
            cliente = Cliente.query.get_or_404(id)
            db.session.delete(cliente)
            db.session.commit()
            return cliente
        except Exception as e:
            db.session.rollback()
            return {"erro": f"Erro ao remover cliente: {str(e)}"}, 500