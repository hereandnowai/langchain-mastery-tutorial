from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import tool
import yfinance as yf
import os
import ast # Abstract Syntax Tree
import time
import sys
from dotenv import load_dotenv

import warnings
warnings.filterwarnings("ignore", message="API key must be provided when using hosted LangSmith API")

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = "models/gemini-2.5-flash-lite-preview-06-17" 

@tool
def get_stock_prices(tickers: str) -> str:
    """
    Fetches the current stock prices for a list of ticker symbols.
    The input should be a string representation of a Python list (e.g., "['GOOG', 'MSFT']").
    Returns the prices in the stock's native currency (USD for US, INR for Indian).
    """
    results = []
    try:
        ticker_list = ast.literal_eval(tickers)
        if not isinstance(ticker_list, list):
            return "Input must be a list of ticker symbols."
    except (ValueError, SyntaxError):
        return "Invalid input format. Please provide a list of tickers as a string (e.g., \"['GOOG', 'RELIANCE.NS']\")."

    for ticker in ticker_list:
        try:
            stock = yf.Ticker(ticker)
            price = stock.info.get('regularMarketPrice')
            if price is None:
                price = stock.history(period="1d")['Close'].iloc[-1] # 1d - one day
            currency = stock.info.get('currency', 'USD')
            results.append(f"The current price of {ticker} is {price:.2f} {currency}. ")
        except Exception as e:
            results.append(f"Could not find the stock price for {ticker}. Error: {e}. ")
    return "".join(results)

def run_finance_agent_stock_price():
    """
    Creates and runs an agent that can use the get_stock_prices tool.
    """
    wait_time = 15
    print(f"Waiting for {wait_time} seconds to comply with potential rate limits...")
    for i in range(wait_time, 0, -1):
        sys.stdout.write(f"\rWaiting... {i} seconds remaining.")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rDone waiting.                          \n")
    # sys.stdout.flush()
    
    llm = ChatGoogleGenerativeAI(model=model, google_api_key=google_api_key)
    tools = [get_stock_prices]
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    response = agent_executor.invoke({
        "input": "What are the current stock prices of Google (GOOG) and Reliance Industries (RELIANCE.NS)?"
    })
    print(response["output"])

if __name__ == "__main__":
    run_finance_agent_stock_price()