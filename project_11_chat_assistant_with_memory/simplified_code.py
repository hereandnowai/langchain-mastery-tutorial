import os
from dotenv import load_dotenv
from config import MODEL

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()
assert os.getenv("GEMINI_API_KEY"), "Set GEMINI_API_KEY in .env"

# Setup LLM and prompt
llm = ChatGoogleGenerativeAI(model=MODEL, google_api_key=os.getenv("GEMINI_API_KEY"))
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")])

# Memory store for session
memory = InMemoryChatMessageHistory()
chat = RunnableWithMessageHistory(prompt | llm, lambda _: memory, input_messages_key="input", history_messages_key="history")

print("🤖 Chatbot (type 'exit' to quit)")
while True:
    user_input = input("You: ")
    if user_input.lower() in ("exit", "quit"):
        break
    response = chat.invoke({"input": user_input},
                           config={"configurable": {"session_id":"default"}})
    print("Bot:", response.content if hasattr(response, "content") else response)