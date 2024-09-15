# Código para gerar dados randomicos e popular a base de dados

import random
from datetime import datetime, timedelta
from contracts import Vendas, ProdutoEnum
from database import salvar_no_postgres

def gerar_dados_aleatorios():
    # Definindo o intervalo de datas (mesma semana)
    data_inicial = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    data_final = data_inicial + timedelta(days=6)
    
    for _ in range(300):  # Gerar 300 registros
        # Gerar email aleatório
        email = f"vendedor{random.randint(1, 100)}@empresa.com"
        
        # Gerar data e hora aleatória dentro do intervalo de uma semana
        data = data_inicial + (data_final - data_inicial) * random.random()
        
        # Gerar valor entre 2000 e 6000
        valor = round(random.uniform(2000, 6000), 2)
        
        # Gerar quantidade entre 1 e 10
        quantidade = random.randint(1, 10)
        
        # Escolher produto aleatório
        produto = random.choice(list(ProdutoEnum))
        
        # Criar objeto de venda
        venda = Vendas(
            email=email,
            data=data,
            valor=valor,
            quantidade=quantidade,
            produto=produto
        )
        
        # Salvar no banco de dados
        salvar_no_postgres(venda)

if __name__ == "__main__":
    gerar_dados_aleatorios()
