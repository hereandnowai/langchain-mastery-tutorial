from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import tool
from dotenv import load_dotenv
import os
import sys
import time
import warnings
warnings.filterwarnings("ignore", message="API key must be provided when using hosted LangSmith API")

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("MODEL")

FACTS = {
    "capital of france": "Paris",
    "largest ocean": "Pacific Ocean",
    "inventor of telephone": "Alexander Graham Bell",
    "population of india": "Approximately 1.4 billion"
}

@tool
def get_fact(query: str) -> str:
    """
    Retrieves a fact from a predefined list. The query must be an exact match
    to one of the available facts.

    Available facts are:
    - 'capital of france'
    - 'largest ocean'
    - 'inventor of telephone'
    - 'population of india'
    """
    return FACTS.get(query.lower(), "Fact not found.")


def run_data_retrieval_agent():
    """
    Creates an agent that can use the get_fact tool.
    """
    llm = ChatGoogleGenerativeAI(model=model, google_api_key=google_api_key)
    tools = [get_fact]
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True
    )
    
    wait_time = 20
    print(f"Agent starting in {wait_time} seconds...")
    for i in range(wait_time, 0, -1):
        sys.stdout.write(f"\rPlease wait for {i} seconds... ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rAgent is running!              \n")
    sys.stdout.flush()

    responses = []
    print("\n--- Query 1: Capital of France ---")
    responses.append(agent_executor.invoke({"input": "What is the capital of France?"}))
    
    print("\n--- Query 2: Inventor of Telephone ---")
    responses.append(agent_executor.invoke({"input": "Who invented the telephone?"}))
    
    print("\n--- Query 3: Population of India ---")
    responses.append(agent_executor.invoke({"input": "What is the population of India?"}))

    print("\n\n--- FINAL AGENT ANSWERS ---")
    for i, response in enumerate(responses, 1):
        print(f"Response {i}: {response['output']}")


if __name__ == "__main__":
    run_data_retrieval_agent()