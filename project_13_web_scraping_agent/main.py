from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = "gemini-1.5-flash-latest"

def run_web_scraping_agent():
    """
    Loads content from a URL, creates a Q&A chain, and answers a question based on its content.
    """
    loader = WebBaseLoader("https://hereandnowai.com/about-here-and-now-ai/")
    documents = loader.load()

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
    question = "Who is the CTO of here and now ai?"
    response = document_chain.invoke({"input": question, "context": documents})

    print(f"Question: {question}")
    print(f"Answer: {response}")

if __name__ == "__main__":
    run_web_scraping_agent()