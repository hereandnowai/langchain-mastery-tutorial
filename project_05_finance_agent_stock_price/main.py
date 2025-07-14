# main.py
# Objective: A very basic agent that can "pretend" to fetch a stock price.

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import tool

# Define a custom tool
@tool
def get_stock_price(ticker: str) -> float:
    """Fetches the current stock price for a given ticker symbol."""
    # In a real application, this would call a financial API.
    # For this example, we return a hardcoded value.
    if ticker.upper() == "GOOG":
        return 150.00
    return 0.00

def run_finance_agent_stock_price():
    """
    Creates an agent that can use the get_stock_price tool.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    tools = [get_stock_price]

    # Get the prompt to use - you can modify this
    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    agent_executor.invoke({"input": "What is the stock price of GOOG?"})

if __name__ == "__main__":
    run_finance_agent_stock_price()
