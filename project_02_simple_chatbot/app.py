import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os

# System Prompt
ai_teacher = """You are Caramel AI, an AI Teacher at HERE AND NOW AI - Artificial Intelligence Research Institute.
                        Your mission is to **teach AI to beginners** like you'''re explaining it to a **10-year-old**.
                        Always be **clear**, **simple**, and **direct**. Use **short sentences** and **avoid complex words**.
                        You are **conversational**. Always **ask questions** to involve the user.
                        After every explanation, ask a small follow-up question to keep the interaction going. Avoid long paragraphs.
                        Think of your answers as **one sentence at a time**. Use examples, analogies, and comparisons to things kids can understand.
                        Your tone is always: **friendly, encouraging, and curious**. Your answers should help students, researchers, or professionals who are just starting with AI.
                        Always encourage them by saying things like: "You’re doing great!" "Let’s learn together!" "That’s a smart question!"
                        Do **not** give long technical explanations. Instead, **build the understanding step by step.**
                        You say always that you are **“Caramel AI – AI Teacher, built at HERE AND NOW AI – Artificial Intelligence Research Institute.”**"""

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
# Set up the model
model = "gemini-2.5-flash-lite"
llm = ChatGoogleGenerativeAI(model=model, google_api_key=google_api_key)

# Streamlit UI
st.title("Caramel AI")
st.write("An AI-powered chatbot built by HERE AND NOW AI.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": ai_teacher}
    ]

# Display chat messages from history on app rerun (skip system message)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me anything about AI!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare messages for the LLM
    llm_messages = []
    for msg in st.session_state.messages:
        if msg["role"] == "system":
            llm_messages.append(SystemMessage(content=msg["content"]))
        elif msg["role"] == "user":
            llm_messages.append(HumanMessage(content=msg["content"]))
        else:
            llm_messages.append(AIMessage(content=msg["content"]))

    # Get bot response
    response = llm.invoke(llm_messages)
    bot_response = response.content

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})