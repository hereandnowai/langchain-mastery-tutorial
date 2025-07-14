# main.py
# Objective: Answer questions about a simple HR policy document.

from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain

def run_hr_policy_qa():
    """
    Loads an HR policy file, creates a Q&A chain, and answers a question based on its content.
    """
    # Load the HR policy document
    loader = TextLoader("hr_policy.txt")
    documents = loader.load()

    # Instantiate the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    # Load the Q&A chain
    chain = load_qa_chain(llm, chain_type="stuff")

    # Ask a question about the HR policy
    question = "How many vacation days do I get?"
    response = chain.invoke({"input_documents": documents, "question": question})

    print(f"Question: {question}")
    print(f"Answer: {response["output_text"]}")

if __name__ == "__main__":
    run_hr_policy_qa()
