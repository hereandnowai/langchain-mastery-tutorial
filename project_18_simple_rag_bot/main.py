# Simple RAG Bot
#
# This script demonstrates a simple Retrieval-Augmented Generation (RAG) bot.
# It loads a knowledge base from a text file, creates a vector store using FAISS,
# and answers questions based on the knowledge base.

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = "gemini-1.5-flash-latest"

# Load the knowledge base
loader = TextLoader("knowledge_base.txt")
documents = loader.load()

# Split the documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

# Create the vector store
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = FAISS.from_documents(docs, embeddings)

# Create the RAG chain
llm = ChatGoogleGenerativeAI(model=model, google_api_key=google_api_key)
prompt = ChatPromptTemplate.from_template(
    """Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}"""
)
document_chain = create_stuff_documents_chain(llm, prompt)

# Ask a question
question = "What is the mission of Here and Now AI?"
retriever = vector_store.as_retriever()
retrieved_documents = retriever.get_relevant_documents(question)
response = document_chain.invoke({"input": question, "context": retrieved_documents})

print(f"Question: {question}")
print(f"Answer: {response}")
