import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = "gemini-1.5-flash-latest"
os.environ["USER_AGENT"] = "langchain-mastery-tutorial/1.0"

def crawl_website(start_url: str, max_pages: int = 10):
    """
    Crawls a website starting from the given URL, up to a maximum number of pages.
    """
    visited = set()
    queue = [start_url]
    documents = []

    while queue and len(visited) < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue

        try:
            response = requests.get(url, headers={"User-Agent": os.environ["USER_AGENT"]})
            response.raise_for_status()
            visited.add(url)

            soup = BeautifulSoup(response.content, "lxml")
            
            # Load content using WebBaseLoader
            loader = WebBaseLoader(url)
            docs = loader.load()
            documents.extend(docs)

            # Find and add new links to the queue
            for link in soup.find_all("a", href=True):
                absolute_link = urljoin(url, link["href"])
                if urlparse(absolute_link).netloc == urlparse(start_url).netloc:
                    if absolute_link not in visited:
                        queue.append(absolute_link)
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")

    return documents

def run_website_qa():
    """
    Crawls a website, creates a Q&A chain, and answers a question based on its content.
    """
    start_url = "https://hereandnowai.com/"
    documents = crawl_website(start_url)

    # Instantiate the LLM
    llm = ChatGoogleGenerativeAI(model=model, google_api_key=google_api_key)

    # Create the prompt template
    prompt = ChatPromptTemplate.from_template(
        """Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}"""
    )

    # Create the stuff documents chain
    document_chain = create_stuff_documents_chain(llm, prompt)

    # Ask a question and get the response
    question = "What are the services offered by here and now ai?"
    response = document_chain.invoke({"input": question, "context": documents})

    print(f"Question: {question}")
    print(f"Answer: {response}")

if __name__ == "__main__":
    run_website_qa()
