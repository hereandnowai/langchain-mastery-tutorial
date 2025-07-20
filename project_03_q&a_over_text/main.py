# main.py
# Objective: Answer questions based on the content of a local text file.

from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = "gemini-1.5-flash"

def run_qa_over_text_file():
    """
    Loads a text file, creates a Q&A chain, and answers a question based on its content.
    """
    # Construct the absolute path to the text file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "about-hereandnowai.txt")

    # Load the document
    loader = TextLoader(file_path)
    documents = loader.load()

    # Instantiate the LLM
    llm = ChatGoogleGenerativeAI(model=model, google_api_key=google_api_key)

    # Create a prompt template
    prompt = ChatPromptTemplate.from_template(
        "Answer the user's question based on the following context:\n\n{context}\n\nQuestion: {input}"
    )

    # Create the Q&A chain
    chain = create_stuff_documents_chain(llm, prompt)

    # Ask a question and get the response
    question = "What is the main product of the company?"
    response = chain.invoke({"context": documents, "input": question})

    print(f"Question: {question}")
    print(f"Answer: {response}")

if __name__ == "__main__":
    run_qa_over_text_file()