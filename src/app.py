import streamlit as st
from contracts import Vendas
from datetime import datetime, time
from pydantic import ValidationError
from database import salvar_no_postgres
from groq_ask import ask_groq
from load_db import carregar_dados_gold_vendas_por_produto, carregar_dados_bronze
import os

# Função para carregar o arquivo CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Carregar o CSS externo
    local_css("src\\assets\\styles.css")  # Certifique-se de que o caminho está correto
    
    # Criação das abas
    tab1, tab2 = st.tabs(["Sistema de Vendas", "Pergunte ao chatGPT"])

    # Aba 1 - Sistema de Vendas
    with tab1:
        st.markdown('<h1 class="main-title">Sistema de CRM e Vendas da XPTO</h1>', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Inserir Venda</h2>', unsafe_allow_html=True)

        # Organização em duas colunas
        col1, col2 = st.columns(2)

        with col1:
            email = st.text_input("Email do vendedor")
            data = st.date_input("Data da compra", datetime.now())
            valor = st.number_input("Valor da venda", min_value=0.0, format="%.2f")

        with col2:
            hora = st.time_input("Hora da compra", value=time(9, 0))
            quantidade = st.number_input("Quantidade de produtos", min_value=1, step=1)
            produto = st.selectbox("Produto", options=["Inteligência com Gemini", "Inteligência com chatGPT", "Inteligência com Llama3.0"])

        # Botão de salvar venda
        st.markdown('<h2 class="section-title">Ações</h2>', unsafe_allow_html=True)
        salvar_col, ver_col = st.columns([2, 1])
        with salvar_col:
            if st.button("Salvar Venda"):
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
                    st.success("Venda salva com sucesso!")
                except ValidationError as e:
                    st.error(f"Erro de validação: {e}")

        with ver_col:
            if st.button("Ver base de dados"):
                df = carregar_dados_bronze()
                st.write(df)

    # Aba 2 - Pergunte ao chatGPT
    with tab2:
        st.markdown('<h1 class="main-title">Pergunte ao chatGPT com Groq</h1>', unsafe_allow_html=True)

        # Formulário de pergunta
        question = st.text_input("Digite sua pergunta", "Qual produto vendeu mais?")
        
        # Mostrar dados em um expander (para economizar espaço)
        with st.expander("Ver dados carregados"):
            df_vendas = carregar_dados_gold_vendas_por_produto()
            if not df_vendas.empty:
                st.write(df_vendas)  # Exibe o DataFrame no Streamlit
            else:
                st.write("Erro ao carregar os dados")

        # Botão de enviar pergunta
        if st.button("Enviar pergunta"):
            df_vendas['data'] = df_vendas['data'].astype(str)
            sales_data_json = df_vendas.to_json(orient='records')
            answer = ask_groq(question, sales_data_json)
            st.write(f"Resposta do Groq: {answer}")

if __name__ == "__main__":
    main()
