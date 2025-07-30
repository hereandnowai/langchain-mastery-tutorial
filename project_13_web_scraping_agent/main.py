import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import tool
from dotenv import load_dotenv
import ast # Abstract Syntax Tree
import warnings

warnings.filterwarnings("ignore", message="API key must be provided when using hosted LangSmith API")

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = "gemini-2.5-flash-lite"

@tool
def web_scrape_tool(urls: str) -> str:
    """
    Scrapes content from a list of URLs.
    The input should be a string representation of a Python list of URLs (e.g., "['https://example.com', 'https://anothersite.com']").
    Returns the concatenated text content of all scraped pages.
    """
    try:
        url_list = ast.literal_eval(urls)
        if not isinstance(url_list, list) or not all(isinstance(url, str) for url in url_list):
            return "Invalid input format. Please provide a list of URLs as a string (e.g., \"['https://example.com']\")."
    except (ValueError, SyntaxError):
        return "Invalid input format. Please provide a list of URLs as a string (e.g., \"['https://example.com']\")."

    combined_content = []
    for url in url_list:
        try:
            loader = WebBaseLoader(
                [url],
                requests_kwargs={"headers": {"User-Agent": "Caramel AI"}}
            )
            documents = loader.load()
            for doc in documents:
                combined_content.append(doc.page_content)
        except Exception as e:
            combined_content.append(f"Could not scrape {url}. Error: {e}. ")
    return "\n\n".join(combined_content)

def run_web_scraping_agent():
    """
    Creates and runs an agent that can use the web_scrape_tool.
    """
    llm = ChatGoogleGenerativeAI(model=model, google_api_key=google_api_key)
    tools = [web_scrape_tool]
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    print("\n--- Query 1: Get content from About Us page ---")
    question_about_us = "What is the content of the 'About Us' page of hereandnowai.com? The URL is https://hereandnowai.com/about-here-and-now-ai/"
    response_about_us = agent_executor.invoke({"input": question_about_us})
    print(f"Agent's response: {response_about_us['output']}")

    print("\n--- Query 2: Summarize content from multiple pages ---")
    question_multi_url = "Please summarize the content from these two pages: https://hereandnowai.com/ and https://hereandnowai.com/contact/"
    response_multi_url = agent_executor.invoke({"input": question_multi_url})
    print(f"Agent's response for multiple URLs: {response_multi_url['output']}")

if __name__ == "__main__":
    run_web_scraping_agent()