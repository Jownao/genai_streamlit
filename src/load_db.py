import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Carregar variáveis de ambiente
load_dotenv()

# Função para conectar ao banco PostgreSQL usando SQLAlchemy
def conectar_db():
    db_url = f"postgresql+psycopg2://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
    engine = create_engine(db_url)
    return engine

# Função para carregar dados em tempo real 
# Não foi utilizado a gold pois pela simplicidade do projeto não é possivel atualizar as camadas automaticamente logo faremos a query diretamente do banco
def carregar_dados_gold_vendas_por_produto():
    engine = conectar_db()
    query = """
WITH vendas_7_dias AS (
    SELECT 
        DATE(data) AS data, 
        produto, 
        SUM(valor) AS total_valor, 
        SUM(quantidade) AS total_quantidade, 
        COUNT(*) AS total_vendas
    FROM 
        vendas
    WHERE
        valor > 1000 
        AND valor < 8000
    GROUP BY 
        data, produto
)

SELECT 
    data, 
    produto, 
    total_valor, 
    total_quantidade, 
    total_vendas
FROM 
    vendas_7_dias
ORDER BY 
    data ASC"""
    dados = pd.read_sql(query, engine)  
    return dados

def carregar_dados_bronze():
    engine = conectar_db()
    query = "SELECT * FROM vendas;"
    dados = pd.read_sql(query, engine)  
    return dados
