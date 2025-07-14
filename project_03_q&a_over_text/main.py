# main.py
# Objective: Answer questions based on the content of a local text file.

from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain

def run_qa_over_text_file():
    """
    Loads a text file, creates a Q&A chain, and answers a question based on its content.
    """
    # Load the document
    loader = TextLoader("sample.txt")
    documents = loader.load()

    # Instantiate the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    # Load the Q&A chain
    chain = load_qa_chain(llm, chain_type="stuff")

    # Ask a question and get the response
    question = "What is the main product of the company?"
    response = chain.invoke({"input_documents": documents, "question": question})

    print(f"Question: {question}")
    print(f"Answer: {response["output_text"]}")

if __name__ == "__main__":
    run_qa_over_text_file()
