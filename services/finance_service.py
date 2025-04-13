import yfinance as yf
from datetime import datetime
import logging
from decimal import Decimal

logging.basicConfig(level=logging.INFO)

class FinanceService:
    @staticmethod
    def get_stock_price(symbol):
        """Busca o preço atual de uma ação usando yfinance"""
        try:
            # Se o símbolo não tiver sufixo, adicione .SA para ações brasileiras
            if '.' not in symbol:
                symbol = f"{symbol}.SA"
                
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if data.empty:
                logging.error(f"Dados não encontrados para o símbolo {symbol}")
                return None
            return float(data['Close'].iloc[-1])
        except Exception as e:
            logging.error(f"Erro ao buscar preço da ação {symbol}: {str(e)}")
            return None
            
    @staticmethod
    def get_currency_price(symbol="USDBRL=X"):
        """Busca o preço atual do dólar em reais"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if data.empty:
                logging.error(f"Dados não encontrados para a moeda {symbol}")
                return None
            return float(data['Close'].iloc[-1])
        except Exception as e:
            logging.error(f"Erro ao buscar cotação da moeda {symbol}: {str(e)}")
            return None
    
    @staticmethod
    def get_portfolio_value(investimentos):
        """Calcula o valor atual da carteira de investimentos"""
        valor_total = 0.0
        for investimento in investimentos:
            try:
                if investimento.tipo == "acao":
                    preco_atual = FinanceService.get_stock_price(investimento.simbolo)
                elif investimento.tipo == "moeda":
                    preco_atual = FinanceService.get_currency_price()
                else:
                    preco_atual = None
                    
                if preco_atual:
                    # Converter ambos os valores para o mesmo tipo (float)
                    quantidade_float = float(investimento.quantidade)
                    preco_float = float(preco_atual)
                    
                    valor_total += preco_float * quantidade_float
                    
            except Exception as e:
                logging.error(f"Erro ao calcular valor para {investimento.simbolo}: {str(e)}")
                
        return valor_total