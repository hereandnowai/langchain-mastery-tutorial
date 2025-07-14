# main.py
# Objective: A finance agent that can retrieve basic company information.

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import tool

# Define a simulated tool for company information
@tool
def get_company_info(company_name: str) -> str:
    """Retrieves basic information about a given company."""
    if company_name.lower() == "google":
        return "Google LLC is an American multinational technology company focusing on online advertising, search engine technology, cloud computing, computer software, quantum computing, e-commerce, artificial intelligence, and consumer electronics."
    elif company_name.lower() == "apple":
        return "Apple Inc. is an American multinational technology company that designs, develops, and sells consumer electronics, computer software, and online services."
    return "Company information not found."

def run_finance_agent_company_info():
    """
    Creates an agent that can use the get_company_info tool.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    tools = [get_company_info]

    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    agent_executor.invoke({"input": "Tell me about Google."})
    agent_executor.invoke({"input": "What is Apple Inc.?"})
    agent_executor.invoke({"input": "Can you tell me about Tesla?"})

if __name__ == "__main__":
    run_finance_agent_company_info()
