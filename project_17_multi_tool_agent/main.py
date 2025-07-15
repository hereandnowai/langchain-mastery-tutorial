"""
Project 17: Multi-tool Agent

Objective: Demonstrate an agent capable of using multiple tools to answer a query.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool, AgentExecutor, AgentType
from datetime import datetime

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro")

# Define tools
def get_current_time(query: str) -> str:
    """Returns the current time."""
    return datetime.now().strftime("%H:%M:%S")

def get_weather_info(query: str) -> str:
    """Returns a hardcoded weather description for a given city."""
    city = query.lower()
    if "london" in city:
        return "It's cloudy with a chance of rain in London."
    elif "new york" in city:
        return "It's sunny and warm in New York."
    else:
        return "Weather information not available for this city."

tools = [
    Tool(
        name="CurrentTime",
        func=get_current_time,
        description="Useful for getting the current time. Input is not used."
    ),
    Tool(
        name="WeatherInfo",
        func=get_weather_info,
        description="Useful for getting weather information for a city. Input should be the city name."
    )
]

# Create an agent executor
agent = AgentExecutor.from_agent_and_tools(
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    verbose=True
)

# Invoke the agent
response = agent.invoke({"input": "What is the current time and what's the weather like in London?"})
print(response["output"])
