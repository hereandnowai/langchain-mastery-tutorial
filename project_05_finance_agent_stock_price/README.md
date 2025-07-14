# Project 5: Finance Agent - Stock Price

## Objective
Create a very basic agent that can "pretend" to fetch a stock price using a custom tool.

## Setup and Run
1.  Navigate to the `project_05_finance_agent_stock_price` directory:
    ```bash
    cd project_05_finance_agent_stock_price
    ```
2.  Install the required dependencies:
    ```bash
    uv pip install -r requirements.txt
    ```
3.  Run the script:
    ```bash
    python main.py
    ```
    The agent will use its tool to answer the stock price query.

## Real-World Value
This project introduces the powerful concept of "agents" in LangChain. Agents are intelligent systems that can decide which tools to use to achieve a goal. Here, we simulate fetching a stock price, but in a real-world scenario, this tool could connect to a live financial API (e.g., Alpha Vantage, Yahoo Finance). This demonstrates how LLMs can go beyond just generating text and interact with external systems, enabling applications like automated financial analysis, personalized investment advice, or real-time market monitoring.
