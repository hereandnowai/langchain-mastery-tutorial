# main.py
# Objective: Create a chat assistant that can remember past conversations.

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

def run_chat_assistant_with_memory():
    """
    Demonstrates a simple chat assistant with conversation memory.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    # Initialize memory
    memory = ConversationBufferMemory()

    # Create a ConversationChain with memory
    conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

    # Simulate a conversation
    print(conversation.predict(input="Hi there!"))
    print(conversation.predict(input="My name is Alice."))
    print(conversation.predict(input="What is my name?"))

if __name__ == "__main__":
    run_chat_assistant_with_memory()
