# main.py
# Objective: An agent that can scrape content from a given URL.

from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from bs4 import BeautifulSoup

def run_web_scraping_agent():
    """
    Loads content from a URL, creates a Q&A chain, and answers a question based on its content.
    """
    # Load the document from a sample URL
    # Note: Replace with a real URL if you want to test live scraping.
    # For demonstration, we'll use a simple local HTML content if no internet access.
    # In a real scenario, you'd pass a URL like "https://www.example.com"
    loader = WebBaseLoader("https://www.example.com")
    documents = loader.load()

    # Instantiate the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    # Load the Q&A chain
    chain = load_qa_chain(llm, chain_type="stuff")

    # Ask a question and get the response
    question = "What is the main heading on this page?"
    response = chain.invoke({"input_documents": documents, "question": question})

    print(f"Question: {question}")
    print(f"Answer: {response["output_text"]}")

if __name__ == "__main__":
    run_web_scraping_agent()
