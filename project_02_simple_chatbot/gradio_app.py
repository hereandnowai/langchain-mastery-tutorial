import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os

# System Prompt for Caramel AI
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

def predict(message, history):
    """Predicts the bot'''s response based on the user'''s message and chat history."""
    history_langchain_format = [SystemMessage(content=ai_teacher)]
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=message))
    
    response = llm.invoke(history_langchain_format)
    return response.content

# Gradio UI
gradio_ui = gr.ChatInterface(predict,
                             title="Caramel AI - Your Friendly AI Teacher",
                             description="Ask me anything about AI! I'''ll explain it simply.",
                             theme="soft",
                             type="messages",
                             examples=["What is a neural network?", 
                                       "How does a computer learn?", 
                                       "Can you tell me about Large Language Models?"])

if __name__ == "__main__":
    gradio_ui.launch()
