# Gemini Command Document for "LangChain from Scratch to Mastery" Tutorial

## 1. Project Overview & Purpose

**Goal:** Generate a complete, well-structured, and beginner-friendly tutorial for building Large Language Model (LLM) applications using LangChain. The tutorial will consist of 20 incremental projects, starting with the basics and progressing to simple, real-world applications.

**Target Audience:** Beginners with some Python knowledge who want to learn LangChain for building LLM-powered apps.

**Core Technologies:**
*   **Programming Language:** Python
*   **Virtual Environment:** uv [12, 33]
*   **Core Framework:** The latest version of LangChain (as of July 14, 2025). [27]
*   **LLM Integration:** Primarily Google Gemini, but also showing how other models can be used.

## 2. Directory and File Layout

Create the following directory structure. Each project folder must contain a `main.py`, a `requirements.txt`, and a `README.md`.


langchain-mastery-tutorial/
|-- .gitignore
|-- branding.json
|-- GEMINI.md
|-- README.md <-- Main project README, generated using branding.json
|-- project_01_hello_langchain/
| |-- main.py
| |-- requirements.txt
| -- README.md |-- project_02_simple_chatbot/ | |-- main.py | |-- requirements.txt |-- README.md
|-- project_03_q&a_over_text/
| |-- main.py
| |-- requirements.txt
| |-- sample.txt
| -- README.md |-- project_04_text_summarizer/ | |-- main.py | |-- requirements.txt |-- README.md
|-- project_05_finance_agent_stock_price/
| |-- main.py
| |-- requirements.txt
| -- README.md |-- project_06_marketing_agent_slogan_generator/ | |-- main.py | |-- requirements.txt |-- README.md
|-- project_07_hr_agent_policy_qa/
| |-- main.py
| |-- requirements.txt
| |-- hr_policy.txt
| -- README.md |-- project_08_simple_data_retrieval_agent/ | |-- main.py | |-- requirements.txt |-- README.md
|-- project_09_question_answering_agent/
| |-- main.py
| |-- requirements.txt
| -- README.md |-- project_10_summarization_pipeline/ | |-- main.py | |-- requirements.txt |-- README.md
|-- project_11_chat_assistant_with_memory/
| |-- main.py
| |-- requirements.txt
| -- README.md |-- project_12_csv_analysis_agent/ | |-- main.py | |-- requirements.txt | |-- sample_data.csv |-- README.md
|-- project_13_web_scraping_agent/
| |-- main.py
| |-- requirements.txt
| -- README.md |-- project_14_finance_agent_company_info/ | |-- main.py | |-- requirements.txt |-- README.md
|-- project_15_marketing_agent_social_media_post/
| |-- main.py
| |-- requirements.txt
| -- README.md |-- project_16_hr_agent_resume_screener/ | |-- main.py | |-- requirements.txt | |-- sample_resume.txt |-- README.md
|-- project_17_multi_tool_agent/
| |-- main.py
| |-- requirements.txt
| -- README.md |-- project_18_simple_rag_bot/ | |-- main.py | |-- requirements.txt | |-- knowledge_base.txt |-- README.md
|-- project_19_sql_querying_agent/
| |-- main.py
| |-- requirements.txt
| |-- sample.db
| -- README.md-- project_20_basic_langgraph_agent/
|-- main.py
|-- requirements.txt
`-- README.md

Generated code
## 3. Coding Conventions and Style

*   **Python Version:** 3.9 or higher.
*   **Code Style:** Follow PEP 8 guidelines.
*   **Variable Naming:** Use clear, descriptive variable names (e.g., `llm_chain` instead of `c`).
*   **Comments:** Be generous with comments. Explain the "why" behind the code, not just the "what". Every `main.py` should start with a block comment explaining the project's purpose.
*   **Code Length:** Each `main.py` file should be no more than 20 lines of Python code, excluding comments and blank lines. This is crucial for beginner readability.
*   **Type Hinting:** Use type hints for all function signatures and variable declarations to improve code clarity and maintainability.
*   **Imports:** Use explicit imports.

## 4. Key Dependencies

For each project's `requirements.txt`, include the necessary libraries. The core dependencies will be:
*   `langchain`
*   `langchain-google-genai`
*   `python-dotenv`
*   `uv`

Other projects will require additional libraries like `langchain-community`, `pandas`, `beautifulsoup4`, `lxml`, etc. Ensure these are listed in the respective `requirements.txt` files.

## 5. Prompt Style for Gemini CLI

When I prompt you, I will use a consistent format. For example, to generate the first project, I will say:

"**Generate Project 1: Hello, LangChain!**"

You should then generate the `main.py`, `requirements.txt`, and `README.md` for that project based on the descriptions below.

## 6. Project Descriptions

Here are the detailed instructions for each of the 20 projects.

---

### **Project 1: Hello, LangChain!**
*   **Objective:** The simplest possible "Hello, World!" to demonstrate a basic LLM call.
*   **`main.py`:**
    *   Import `ChatGoogleGenerativeAI`.
    *   Instantiate the model.
    *   Invoke the model with a simple prompt like "Tell me a fun fact about the Roman Empire."
    *   Print the response.
*   **`README.md`:** Explain the goal of this project, how to set up the environment, and how to run the script. Include a "Real-World Value" section explaining that this is the foundational block for any LLM application.

### **Project 2: Simple Chatbot**
*   **Objective:** Create a basic interactive chatbot that takes user input.
*   **`main.py`:**
    *   Use a `while` loop to continuously prompt the user for input.
    *   Feed the user's input to the LLM.
    *   Print the LLM's response.
    *   Include a way to exit the loop (e.g., typing "quit").
*   **`README.md`:** Explain the chatbot functionality and how it differs from the first project. The "Real-World Value" can touch on customer service bots.

### **Project 3: Q&A Over a Text File**
*   **Objective:** Answer questions based on the content of a local text file.
*   **`main.py`:**
    *   Use `TextLoader` to load a `sample.txt` file.
    *   Create a simple chain that takes a question and the document context.
*   **`sample.txt`:** Include a short paragraph about a fictional company.
*   **`README.md`:** Explain how to use local data with LangChain. The "Real-World Value" can be about querying internal documentation.

### **Project 4: Text Summarizer**
*   **Objective:** Summarize a given piece of text.
*   **`main.py`:**
    *   Create a prompt template for summarization.
    *   Use an `LLMChain` to combine the prompt and the model.
    *   Provide a long string of text and print the summary.
*   **`README.md`:** Describe the concept of prompt templates and chains. The "Real-World Value" can be about summarizing articles, emails, or reports.

### **Project 5: Finance Agent - Stock Price**
*   **Objective:** A very basic agent that can "pretend" to fetch a stock price.
*   **`main.py`:**
    *   Create a simple function that returns a hardcoded stock price for a given ticker.
    *   Convert this function into a `Tool`.
    *   Create an agent that can use this tool.
*   **`README.md`:** Introduce the concept of agents and tools. The "Real-World Value" is about creating agents that can interact with financial data APIs.

### **Project 6: Marketing Agent - Slogan Generator**
*   **Objective:** Generate marketing slogans for a product.
*   **`main.py`:**
    *   Create a prompt template that takes a product name and description.
    *   The prompt should ask the LLM to generate 5 creative slogans.
*   **`README.md`:** Discuss the power of prompt engineering for creative tasks. The "Real-World Value" is about using LLMs for marketing content creation.

### **Project 7: HR Agent - Policy Q&A**
*   **Objective:** Answer questions about a simple HR policy document.
*   **`main.py`:**
    *   Similar to Project 3, but specifically for an "HR" use case.
    *   Load an `hr_policy.txt` file.
    *   Answer a question like "How many vacation days do I get?".
*   **`hr_policy.txt`:** A short text outlining a basic vacation policy.
*   **`README.md`:** Reinforce the concept of Q&A over documents with a practical business example. The "Real-World Value" is about building HR assistants.

### **And so on for projects 8 through 20, with increasing complexity...**

**(You would continue this pattern for all 20 projects, introducing concepts like different types of chains, agents with multiple tools, memory, RAG, and basic LangGraph.)**

---

### **Project 18: Simple RAG Bot**
*   **Objective:** Build a basic Retrieval-Augmented Generation bot.
*   **`main.py`:**
    *   Load a `knowledge_base.txt`.
    *   Use `RecursiveCharacterTextSplitter` to chunk the document.
    *   Use `FAISS` (or another simple vector store) and `GoogleGenerativeAIEmbeddings`.
    *   Create a retrieval chain.
*   **`knowledge_base.txt`:** A slightly longer document with more detailed information.
*   **`README.md`:** Explain the concept of RAG and why it's powerful for reducing hallucinations and using up-to-date information.

### **Project 20: Basic LangGraph Agent**
*   **Objective:** Introduce the concept of building cyclical and stateful applications with LangGraph.
*   **`main.py`:**
    *   Define a simple graph with a couple of nodes.
    *   The graph should take an initial state and transition between nodes based on some logic.
*   **`README.md`:** Provide a high-level overview of LangGraph and its benefits for creating more complex and robust agents.

## 7. Main `README.md` Generation

Generate a `README.md` file for the root directory. This file should be visually appealing and professional.

*   **Use the `branding.json` file provided.**
    *   The `organizationLongName` should be the main title.
    *   Include the `logo.title` image.
    *   Use the `slogan`.
    *   List the `website`, `email`, and `mobile` contact information.
    *   Link to all the `socialMedia` profiles.
*   **Content:**
    *   A brief introduction to the tutorial and its goals.
    *   A "Why LangChain?" section.
    *   "How to Use This Tutorial" section, explaining the `uv` virtual environment setup.
    *   A table of contents linking to each of the 20 project directories.
    *   A "Contributing" section.
    *   A "License" section (e.g., MIT).

## 8. Final Instructions

*   Ensure all Python code is well-commented and easy for a beginner to understand.
*   The "Real-World Value" section in each project's `README.md` is critical for helping learners connect the concepts to practical applications.
*   Double-check that all file paths and commands are correct for a standard Unix-like environment. Provide alternatives for Windows where necessary (e.g., for activating the virtual environment).