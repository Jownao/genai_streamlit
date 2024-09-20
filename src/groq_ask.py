import os
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Configure sua chave de API como uma variável de ambiente
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Função para enviar uma pergunta ao Groq com os dados em JSON
def ask_groq(question, data_json):
    # Cria o conteúdo da mensagem com a pergunta e os dados em JSON
    content = {
        "question": ("Você recebe uma base de dados e só precisa responder oque foi perguntado, nada de códigos, apenas cálculos referente a pergunta.\n",question),
        "sales_data": data_json
    }
    # Envia a pergunta e os dados ao Groq
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": str(content)}],
        model="llama3-8b-8192"  # Certifique-se de escolher o modelo correto
    )
    # Extraindo o conteúdo da resposta
    return chat_completion.choices[0].message.content

