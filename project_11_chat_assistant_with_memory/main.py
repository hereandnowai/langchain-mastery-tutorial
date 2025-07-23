import os
from dotenv import load_dotenv
from config import MODEL

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from pydantic import BaseModel, Field
from langchain_core.rate_limiters import InMemoryRateLimiter

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = MODEL

class SlidingHistory(BaseChatMessageHistory, BaseModel):
    messages: list = Field(default_factory=list)
    k: int = Field(default=5)

    def add_messages(self, msgs: list[HumanMessage | AIMessage]) -> None:
        self.messages.extend(msgs)
        self.messages = self.messages[-self.k:]

    def clear(self) -> None:
        self.messages = []

# session storage for histories
store: dict[str, SlidingHistory] = {}

def get_session_history(session_id: str) -> SlidingHistory:
    if session_id not in store:
        store[session_id] = SlidingHistory(k=5)
    return store[session_id]

def run_chat_assistant_with_memory(session_id: str = "default_session"):
    """
    Modern chat assistant with sliding-window memory (last 5 messages).
    """

    rate_limiter = InMemoryRateLimiter(
        requests_per_second=0.1,
        check_every_n_seconds=0.1,
        max_bucket_size=1
    )

    llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=google_api_key,
        rate_limiter=rate_limiter,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    # Build a runnable chain: prompt → LLM
    chain = prompt | llm

    # Wrap with history tracking
    with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    # Simulate conversation
    for user_input in ["Hi there!", "My name is Alice.", "What is my name?"]:
        res = with_history.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        print("User:", user_input)
        print("AI  :", getattr(res, "content", res))

if __name__ == "__main__":
    run_chat_assistant_with_memory()