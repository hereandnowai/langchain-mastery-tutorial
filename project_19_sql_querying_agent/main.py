# SQL Querying Agent
#
# This script demonstrates a SQL querying agent that can answer questions about a database.
# It uses a SQLDatabase object to connect to the database and a create_sql_query_chain
# to generate and execute SQL queries.

import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = "gemini-1.5-flash-latest"

# Connect to the database
db = SQLDatabase.from_uri("sqlite:///sample.db")

# Create the SQL query chain
llm = ChatGoogleGenerativeAI(model=model, google_api_key=google_api_key)
chain = create_sql_query_chain(llm, db)

# Ask a question
question = "How many users are there?"
response = chain.invoke({"question": question})

print(f"Question: {question}")
print(f"SQL Query: {response}")
