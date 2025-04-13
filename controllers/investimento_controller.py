from models.cliente import db, Cliente
from models.investimento import Investimento
from services.finance_service import FinanceService
from datetime import datetime
from decimal import Decimal

class InvestimentoController:
    @staticmethod
    def listar_investimentos(cliente_id):
        """Lista todos os investimentos de um cliente"""
        return Investimento.query.filter_by(cliente_id=cliente_id).all()
    
    @staticmethod
    def listar_investimentos_agregados(cliente_id):
        """Lista os investimentos de um cliente, agregando ativos do mesmo tipo e símbolo"""
        investimentos = Investimento.query.filter_by(cliente_id=cliente_id).all()
        
        # Dicionário para agregar por tipo e símbolo
        investimentos_agregados = {}
        
        for inv in investimentos:
            chave = f"{inv.tipo}:{inv.simbolo}"
            
            if chave not in investimentos_agregados:
                # Criamos uma cópia do investimento para agregação
                investimentos_agregados[chave] = {
                    "id": inv.id,  # Mantemos o ID do primeiro registro encontrado
                    "cliente_id": inv.cliente_id,
                    "tipo": inv.tipo,
                    "simbolo": inv.simbolo,
                    "quantidade": inv.quantidade,
                    "preco_compra": inv.preco_compra,  # Esse será o preço médio depois
                    "valor_investido": inv.quantidade * inv.preco_compra,
                    "data_compra": inv.data_compra
                }
            else:
                # Somamos a quantidade e atualizamos o preço médio
                atual = investimentos_agregados[chave]
                nova_quantidade = atual["quantidade"] + inv.quantidade
                novo_valor = atual["valor_investido"] + (inv.quantidade * inv.preco_compra)
                
                atual["quantidade"] = nova_quantidade
                atual["valor_investido"] = novo_valor
                atual["preco_compra"] = novo_valor / nova_quantidade  # Preço médio ponderado
                
                # Usamos a data mais recente
                if inv.data_compra > atual["data_compra"]:
                    atual["data_compra"] = inv.data_compra
        
        # Convertemos o dicionário de volta para lista
        return list(investimentos_agregados.values())
    
    @staticmethod
    def obter_investimento(id):
        """Obtém um investimento específico pelo ID"""
        return Investimento.query.get_or_404(id)
    
    @staticmethod
    def comprar_acao(cliente_id, data):
        """Compra ações para um cliente"""
        try:
            cliente = Cliente.query.get_or_404(cliente_id)
            simbolo = data['simbolo']
            quantidade = float(data['quantidade'])
            
            # Verificar quantidade válida
            if quantidade <= 0:
                return {"erro": "A quantidade deve ser um valor positivo"}, 400
            
            # Obter preço atual da ação
            preco_atual = FinanceService.get_stock_price(simbolo)
            if preco_atual is None:
                return {"erro": f"Não foi possível obter o preço para a ação {simbolo}"}, 400
            
            # Calcular valor total da compra
            valor_total = Decimal(str(preco_atual * quantidade))
            
            # Verificar saldo suficiente
            if cliente.saldo < valor_total:
                return {"erro": f"Saldo insuficiente. Necessário: R$ {valor_total:.2f}, Disponível: R$ {cliente.saldo:.2f}"}, 400
            
            # Criar o investimento
            investimento = Investimento(
                cliente_id=cliente_id,
                tipo="acao",
                simbolo=simbolo,
                quantidade=quantidade,
                preco_compra=preco_atual
            )
            
            # Atualizar saldo do cliente
            cliente.saldo -= valor_total
            
            # Persistir no banco
            db.session.add(investimento)
            db.session.commit()
            
            return investimento, 201
        except Exception as e:
            db.session.rollback()
            return {"erro": f"Erro na operação de compra de ações: {str(e)}"}, 500
    
    @staticmethod
    def comprar_dolar(cliente_id, data):
        """Compra dólares para um cliente"""
        try:
            cliente = Cliente.query.get_or_404(cliente_id)
            quantidade = float(data['quantidade'])
            
            # Verificar quantidade válida
            if quantidade <= 0:
                return {"erro": "A quantidade deve ser um valor positivo"}, 400
            
            # Obter cotação atual do dólar
            cotacao_atual = FinanceService.get_currency_price()
            if cotacao_atual is None:
                return {"erro": "Não foi possível obter a cotação do dólar"}, 400
            
            # Calcular valor total em reais
            valor_total = Decimal(str(cotacao_atual * quantidade))
            
            # Verificar saldo suficiente
            if cliente.saldo < valor_total:
                return {"erro": f"Saldo insuficiente. Necessário: R$ {valor_total:.2f}, Disponível: R$ {cliente.saldo:.2f}"}, 400
            
            # Criar o investimento
            investimento = Investimento(
                cliente_id=cliente_id,
                tipo="moeda",
                simbolo="USD",
                quantidade=quantidade,
                preco_compra=cotacao_atual
            )
            
            # Atualizar saldo do cliente
            cliente.saldo -= valor_total
            
            # Persistir no banco
            db.session.add(investimento)
            db.session.commit()
            
            return investimento, 201
        except Exception as e:
            db.session.rollback()
            return {"erro": f"Erro na operação de compra de dólares: {str(e)}"}, 500
    
    @staticmethod
    def calcular_valor_carteira(cliente_id):
        """Calcula o valor atual da carteira de investimentos do cliente"""
        investimentos = Investimento.query.filter_by(cliente_id=cliente_id).all()
        valor_atual = FinanceService.get_portfolio_value(investimentos)
        return {"cliente_id": cliente_id, "valor_carteira": valor_atual}