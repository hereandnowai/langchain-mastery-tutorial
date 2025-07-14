# main.py
# Objective: The simplest possible "Hello, World!" to demonstrate a basic LLM call.

from langchain_google_genai import ChatGoogleGenerativeAI

def run_hello_langchain():
    """
    Instantiates a ChatGoogleGenerativeAI model and invokes it with a simple prompt.
    Prints the model's response.
    """
    # Instantiate the model
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    # Invoke the model with a simple prompt
    response = llm.invoke("Tell me a fun fact about the Roman Empire.")

    # Print the response
    print(response.content)

if __name__ == "__main__":
    run_hello_langchain()
