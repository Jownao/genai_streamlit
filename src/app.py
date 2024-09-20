import streamlit as st
from contracts import Vendas
from datetime import datetime, time
from pydantic import ValidationError
from database import salvar_no_postgres
from groq_ask import ask_groq
from load_db import carregar_dados_gold_vendas_por_produto,carregar_dados_bronze

def main():
    # Criação das abas
    tab1, tab2 = st.tabs(["Sistema de Vendas", "Pergunte ao chatGPT"])

    # Aba 1 - Sistema de Vendas
    with tab1:
        st.title("Sistema de CRM e Vendas da XPTO - Frontend Simples")
        email = st.text_input("Campo de texto para inserção do email do vendedor")
        data = st.date_input("Data da compra", datetime.now())
        hora = st.time_input("Hora da compra", value=time(9, 0))
        valor = st.number_input("Valor da venda", min_value=0.0, format="%.2f")
        quantidade = st.number_input("Quantidade de produtos", min_value=1, step=1)
        produto = st.selectbox("Produto", options=["Inteligência com Gemini", "Inteligência com chatGPT", "Inteligência com Llama3.0"])

        if st.button("Salvar"):
            try:
                data_hora = datetime.combine(data, hora)
                venda = Vendas(
                    email=email,
                    data=data_hora,
                    valor=valor,
                    quantidade=quantidade,
                    produto=produto
                )
                st.write(venda)
                salvar_no_postgres(venda)
            except ValidationError as e:
                st.error(f"Erro de validação: {e}")
        if st.button("Ver base de dados"):
            df = carregar_dados_bronze()
            st.write(df)
    # Aba 2 - Pergunte ao chatGPT
    with tab2:
        st.title("Pergunte ao chatGPT com Groq")
        question = st.text_input("Digite sua pergunta", "Qual produto vendeu mais?")

        # Carregar os dados diretamente do banco em tempo real
        df_vendas = carregar_dados_gold_vendas_por_produto()

        if not df_vendas.empty:
            st.write(df_vendas)  # Exibe o DataFrame no Streamlit
        else:
            st.write("Erro ao carregar os dados")

        if st.button("Enviar pergunta"):
            sales_data_json = df_vendas.to_json(orient='records')
            answer = ask_groq(question, sales_data_json)
            st.write(f"Resposta do Groq: {answer}")

if __name__=="__main__":
    main()