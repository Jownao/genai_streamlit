import streamlit as st
from contracts import Vendas
from datetime import datetime, time
from pydantic import ValidationError
from database import salvar_no_postgres
from groq_ask import ask_groq
from load_db import carregar_dados_gold_vendas_por_produto,carregar_dados_bronze


df_vendas = carregar_dados_gold_vendas_por_produto()
#df_vendas['data'] = df_vendas['data'].apply(lambda x: x.strftime("%Y-%m-%d") if isinstance(x, datetime) else x)
df_vendas['data'] = df_vendas['data'].astype(str)

sales_data_json = df_vendas.to_json(orient='records')

#print(df_vendas.head())
#print(df_vendas.dtypes)
print(sales_data_json)