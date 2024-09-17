from groq import Groq
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

# Função para fazer perguntas ao assistente Groq
def ask_groq(question):
    # Definir o prompt do sistema
    system_prompt = {
        "role": "system",
        "content": "You are a helpful assistant. You reply with very short answers."
    }

    # Inicializar o histórico de chat com o prompt do sistema
    chat_history = [system_prompt]

    # Adicionar a pergunta do usuário ao histórico
    chat_history.append({"role": "user", "content": question})

    # Fazer a chamada para o modelo da API Groq
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=chat_history,
        max_tokens=100,
        temperature=1.2
    )

    # Adicionar a resposta do assistente ao histórico
    chat_history.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })

    # Retornar a resposta do assistente
    return response.choices[0].message.content

# Exemplo de uso da função
question = input("Digite sua pergunta: ")
answer = ask_groq(question)
print("Assistant:", answer)
