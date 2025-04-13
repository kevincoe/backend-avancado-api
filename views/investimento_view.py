from flask import Blueprint, request, jsonify
from controllers.investimento_controller import InvestimentoController
from schemas.investimento_schema import InvestimentoSchema

investimento_bp = Blueprint('investimento_bp', __name__)
investimento_schema = InvestimentoSchema()
investimentos_schema = InvestimentoSchema(many=True)

@investimento_bp.route('/clientes/<int:cliente_id>/investimentos', methods=['GET'])
def listar_investimentos(cliente_id):
    """Lista todos os investimentos de um cliente"""
    investimentos = InvestimentoController.listar_investimentos(cliente_id)
    return jsonify(investimentos_schema.dump(investimentos))

@investimento_bp.route('/clientes/<int:cliente_id>/investimentos/carteira', methods=['GET'])
def obter_valor_carteira(cliente_id):
    """Obtém o valor atual da carteira de investimentos"""
    valor_carteira = InvestimentoController.calcular_valor_carteira(cliente_id)
    return jsonify(valor_carteira)

@investimento_bp.route('/clientes/<int:cliente_id>/investimentos/acoes', methods=['POST'])
def comprar_acao(cliente_id):
    """Compra ações para um cliente"""
    data = request.get_json()
    resultado, status_code = InvestimentoController.comprar_acao(cliente_id, data)
    
    if isinstance(resultado, dict) and "erro" in resultado:
        return jsonify(resultado), status_code
        
    return jsonify(investimento_schema.dump(resultado)), status_code

@investimento_bp.route('/clientes/<int:cliente_id>/investimentos/agregados', methods=['GET'])
def listar_investimentos_agregados(cliente_id):
    """Lista todos os investimentos de um cliente, agregando ativos do mesmo tipo e símbolo"""
    investimentos = InvestimentoController.listar_investimentos_agregados(cliente_id)
    return jsonify(investimentos)

@investimento_bp.route('/clientes/<int:cliente_id>/investimentos/dolar', methods=['POST'])
def comprar_dolar(cliente_id):
    """Compra dólares para um cliente"""
    data = request.get_json()
    resultado, status_code = InvestimentoController.comprar_dolar(cliente_id, data)
    
    if isinstance(resultado, dict) and "erro" in resultado:
        return jsonify(resultado), status_code
        
    return jsonify(investimento_schema.dump(resultado)), status_code