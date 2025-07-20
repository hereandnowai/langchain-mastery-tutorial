<div align="center">
  <a href="https://www.hereandnow.ai/">
    <img src="https://img.shields.io/badge/Here_and_Now_AI-Tutorial_Series-blue.svg" alt="Here and Now AI Tutorial Series">
  </a>
  <h1>Project 5: Finance Agent - Stock Price</h1>
  <strong>A deep dive into creating your first LangChain Agent with a custom tool.</strong>
</div>

---

## 🌟 Project Objective

Welcome to Project 5! This isn't just another script; it's your first step into the exciting world of **LangChain Agents**. An agent is an AI system that doesn't just respond to you—it can **think, decide, and use tools** to accomplish a goal.

In this project, we will build a simple but powerful financial agent. Its mission is to answer the question: *"What is the current stock price of a company?"* To do this, we will write a custom Python function to fetch stock data and then give that function to our agent as a **Tool**.

## 🚀 How to Run This Project

Getting started is easy. Just follow these steps in your terminal.

1.  **Navigate to the project directory:**
    ```bash
    cd project_05_finance_agent_stock_price
    ```
2.  **Install the necessary Python libraries:**
    *(We use `uv` for a fast and modern virtual environment setup.)*
    ```bash
    uv pip install -r requirements.txt
    ```
3.  **Run the main script:**
    ```bash
    python main.py
    ```

You will see the agent "think" out loud in your terminal, decide to use the stock price tool, get the result, and give you a final answer.

---

## 🧠 Deep Dive: Understanding the Code (`main.py`)

Let's break down the `main.py` file line-by-line. Understanding every piece is key to mastering agents.

### 1. The Imports: Gathering Our Libraries

```python
import os
import ast
import time
import sys
from dotenv import load_dotenv
import warnings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import tool
import yfinance as yf
```

*   `os`: Used to access environment variables, like your `GEMINI_API_KEY`.
*   `ast`: Stands for **Abstract Syntax Tree**. We use its `literal_eval` function to safely convert a string that looks like a list (e.g., `"['GOOG', 'MSFT']"`) into an actual Python list. This is crucial for security, as the powerful `eval()` function could run malicious code.
*   `time` & `sys`: Used to create the interactive countdown timer you see when you run the script. `sys` lets us write to the same line in the terminal.
*   `dotenv`: Loads your secret API key from the `.env` file so you don't have to hardcode it.
*   `warnings`: We use this to hide a common, harmless warning from LangChain about LangSmith API keys, keeping our output clean.
*   `langchain_...` & `yfinance`: These are the core libraries for our project. We import the Google Gemini model, the agent-building components, the `@tool` decorator, and the Yahoo Finance library to get real stock data.

### 2. The Setup: Preparing the Environment

```python
warnings.filterwarnings("ignore", message="API key must be provided when using hosted LangSmith API")
load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = "models/gemini-2.5-flash-lite-preview-06-17"
```

Here, we simply tell Python to ignore a specific warning, load our environment variables from the `.env` file, and store our API key and the chosen Gemini model name in variables for later use.

### 3. The Tool: `get_stock_prices()`

This is the most important concept in this project. A **Tool** is a function that an agent can decide to use to get information or perform an action.

```python
@tool
def get_stock_prices(tickers: str) -> str:
    """
    Fetches the current stock prices for a list of ticker symbols.
    The input should be a string representation of a Python list (e.g., "['GOOG', 'MSFT']").
    Returns the prices in the stock's native currency (USD for US, INR for Indian).
    """
    # ... function code ...
```

#### **❓ What is the `@tool` decorator?**

The `@tool` line is a **decorator**. It's a special piece of Python syntax that wraps the function below it, giving it extra powers. In this case, it registers our `get_stock_prices` function with LangChain, making it an official "Tool" that an agent can see and use.

#### **❓ Why is the docstring `"""..."""` so important?**

The text right below the function definition is called a **docstring**. For a LangChain tool, this is **critical**. The agent's "brain" (the LLM) reads this docstring to understand what the tool does. Based on this description, it decides if this tool is the right one to use to answer the user's question. A good docstring is the key to a smart agent.

#### **Code Breakdown:**

*   `ticker_list = ast.literal_eval(tickers)`: Safely converts the input string from the agent (e.g., `"['GOOG']"`) into a real list (`['GOOG']`).
*   `stock = yf.Ticker(ticker)`: Creates an object to interact with the Yahoo Finance API for a specific stock.
*   `price = stock.info.get('regularMarketPrice')`: The fastest way to get the current price.
*   `if price is None:`: Sometimes, `regularMarketPrice` isn't available. This is our fallback.
*   `price = stock.history(period="1d")['Close'].iloc[-1]`: This is a powerful line using the `pandas` library. It means: "Fetch the last **1 day** of stock data, get the **'Close'** price column, and give me the very last entry (`.iloc[-1]`)."
*   `results.append(f"...")`: We build a nice, human-readable string.
*   `{price:.2f}`: This is an **f-string format specifier**. It tells Python to format the `price` variable as a floating-point number with exactly **2** decimal places.
*   `return "".join(results)`: Finally, we join all the individual result strings into a single block of text to return to the agent.

### 4. The Orchestrator: `run_finance_agent_stock_price()`

If `get_stock_prices` is the **Tool**, this function is the **Orchestrator** (or the "Carpenter") that sets up the agent and puts it to work.

#### **❓ Why do we need two separate functions?**

This separation is key to good design.
*   **The Tool (`get_stock_prices`)** is a self-contained, reusable capability. It doesn't know about agents or LLMs.
*   **The Orchestrator (`run_finance_agent_stock_price`)** assembles the AI system. It chooses the brain (LLM) and the tools, and gives the agent a task.

This design makes it easy to add more tools to your agent later without rewriting everything.

#### **Code Breakdown:**

```python
def run_finance_agent_stock_price():
    # ... countdown timer code ...

    llm = ChatGoogleGenerativeAI(model=model, google_api_key=google_api_key)
    tools = [get_stock_prices]
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    response = agent_executor.invoke({
        "input": "What are the current stock prices of Google (GOOG) and Reliance Industries (RELIANCE.NS)?"
    })
    print(response["output"])
```

1.  `llm = ...`: We initialize our "brain," the Gemini model.
2.  `tools = [get_stock_prices]`: We put our tool(s) into a list for the agent to use.
3.  `prompt = hub.pull("hwchase17/react")`: We pull a pre-built prompt template from the LangChain Hub. The "react" prompt is a famous template that teaches an agent how to **Re**ason and **Act**. It guides the agent through a `Thought -> Action -> Observation` loop.
4.  `agent = create_react_agent(...)`: We assemble the agent, giving it the LLM, the tools, and the prompt that teaches it how to think.
5.  `agent_executor = AgentExecutor(...)`: This is the engine that actually runs the agent loop. `verbose=True` is amazing for learning—it makes the agent print out its thoughts and actions step-by-step.
6.  `agent_executor.invoke(...)`: We give the agent its task and kick it off!

### 5. The Entry Point

```python
if __name__ == "__main__":
    run_finance_agent_stock_price()
```

This is standard Python practice. It means "only run the `run_finance_agent_stock_price()` function if this script is executed directly." It prevents the code from running automatically if it's imported into another file.

---

## 💼 Real-World Value

This project is the "Hello, World!" of AI agents. The concept you've learned here—giving an LLM tools to interact with the outside world—is the foundation for building incredibly powerful applications:

*   **Automated Financial Analysis:** An agent could use tools to fetch stock prices, read company news, and analyze financial reports to generate a summary.
*   **Customer Service Bots:** An agent could use a tool to look up a customer's order status in a database.
*   **Smart Home Assistants:** An agent could use tools to control your lights, thermostat, and music.

You've taken your first step into a larger world of building AI that doesn't just talk, but *does*.

---

<div align="center">
  <h2>Connect with Here and Now AI</h2>
  <p>Your journey into AI and LLMs is just beginning. Follow us for more tutorials, projects, and insights!</p>
  <a href="https://www.youtube.com/@hereandnowai"><img src="https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white" alt="YouTube"></a>
  <a href="https://github.com/hereandnow-ai"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="https://www.linkedin.com/in/hereandnowai/"><img src="https://img.shields.io/badge/LinkedIn-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="https://x.com/hereandnow_ai"><img src="https://img.shields.io/badge/Twitter-%231DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=white" alt="Twitter"></a>
  <br>
  <strong>Website:</strong> <a href="https://www.hereandnow.ai">www.hereandnow.ai</a> | <strong>Contact:</strong> <a href="mailto:info@hereandnow.ai">info@hereandnow.ai</a>
</div>