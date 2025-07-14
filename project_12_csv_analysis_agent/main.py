# main.py
# Objective: Analyze a CSV file using an agent.

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import pandas as pd

def run_csv_analysis_agent():
    """
    Creates a CSV agent to answer questions about data in a CSV file.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    # Create a dummy CSV file for demonstration
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'City': ['New York', 'London', 'Paris', 'Tokyo'],
        'Salary': [70000, 80000, 90000, 100000]
    }
    df = pd.DataFrame(data)
    df.to_csv("sample_data.csv", index=False)

    # Create the CSV agent
    agent = create_csv_agent(llm, "sample_data.csv", verbose=True)

    # Ask questions to the agent
    agent.invoke("How many people are in New York?")
    agent.invoke("What is the average salary?")

if __name__ == "__main__":
    run_csv_analysis_agent()
