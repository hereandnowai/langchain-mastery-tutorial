# main.py
# Objective: A basic agent that can retrieve data from a predefined list of facts.

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import tool

# Define a simple data source (e.g., a dictionary of facts)
FACTS = {
    "capital of france": "Paris",
    "largest ocean": "Pacific Ocean",
    "inventor of telephone": "Alexander Graham Bell",
    "population of india": "Approximately 1.4 billion"
}

@tool
def get_fact(query: str) -> str:
    """Retrieves a fact based on the query."""
    return FACTS.get(query.lower(), "Fact not found.")

def run_data_retrieval_agent():
    """
    Creates an agent that can use the get_fact tool.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    tools = [get_fact]

    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    agent_executor.invoke({"input": "What is the capital of France?"})
    agent_executor.invoke({"input": "Who invented the telephone?"})
    agent_executor.invoke({"input": "What is the population of China?"})

if __name__ == "__main__":
    run_data_retrieval_agent()
