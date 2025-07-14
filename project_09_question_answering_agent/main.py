# main.py
# Objective: A more advanced Q&A agent that can answer general knowledge questions.

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

def run_qa_agent():
    """
    Creates an agent that can use the Wikipedia tool to answer questions.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    # Set up Wikipedia tool
    wikipedia_api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
    wikipedia_tool = WikipediaQueryRun(api_wrapper=wikipedia_api_wrapper)
    tools = [wikipedia_tool]

    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    agent_executor.invoke({"input": "Who is the current president of the United States?"})
    agent_executor.invoke({"input": "What is the capital of Japan?"})

if __name__ == "__main__":
    run_qa_agent()
