from groq import Groq
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)
# Set the system prompt
system_prompt = {
    "role": "system",
    "content":
    "You are a helpful assistant. You reply with very short answers."
}

# Initialize the chat history
chat_history = [system_prompt]

while True:
  # Get user input from the console
  user_input = input("You: ")

  # Append the user input to the chat history
  chat_history.append({"role": "user", "content": user_input})

  response = client.chat.completions.create(model="llama3-8b-8192",
                                            messages=chat_history,
                                            max_tokens=100,
                                            temperature=1.2)
  # Append the response to the chat history
  chat_history.append({
      "role": "assistant",
      "content": response.choices[0].message.content
  })
  # Print the response
  print("Assistant:", response.choices[0].message.content)





''' temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,'''
