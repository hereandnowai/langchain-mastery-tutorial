# main.py
# Objective: The simplest possible "Hello, World!" to demonstrate a basic LLM call.

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = "gemini-2.5-flash-lite"

def run_hello_langchain():
    """
    Instantiates a ChatGoogleGenerativeAI model and invokes it with a simple prompt.
    Prints the model's response.
    """
    # Instantiate the model
    llm = ChatGoogleGenerativeAI(model=model, google_api_key=google_api_key)

    # Invoke the model with a simple prompt
    response = llm.invoke("Explain back propagation in 2 lines?")

    # Print the response
    print(response.content)

if __name__ == "__main__":
    run_hello_langchain()