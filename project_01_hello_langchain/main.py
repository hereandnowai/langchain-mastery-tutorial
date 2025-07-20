# main.py
# Objective: The simplest possible "Hello, World!" to demonstrate a basic LLM call.

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def run_hello_langchain():
    """
    Instantiates a ChatGoogleGenerativeAI model and invokes it with a simple prompt.
    Prints the model's response.
    """
    # Instantiate the model
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

    # Invoke the model with a simple prompt
    response = llm.invoke("Tell me about HERE AND NOW AI - Artificial Intelligence Research Institute")

    # Print the response
    print(response.content)

if __name__ == "__main__":
    run_hello_langchain()