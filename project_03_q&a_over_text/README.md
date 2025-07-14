# Project 3: Q&A Over a Text File

## Objective
Answer questions based on the content of a local text file (`sample.txt`).

## Setup and Run
1.  Navigate to the `project_03_q&a_over_text` directory:
    ```bash
    cd "project_03_q&a_over_text"
    ```
2.  Install the required dependencies:
    ```bash
    uv pip install -r requirements.txt
    ```
3.  Run the script:
    ```bash
    python main.py
    ```
    The script will ask you a question about the `sample.txt` content.

## Real-World Value
This project demonstrates how to leverage LangChain to extract information and answer questions from your own local documents. This is incredibly valuable for use cases like querying internal company documentation, analyzing research papers, or building knowledge bases from unstructured text data. It allows you to unlock insights from your private data without sending it to external LLM providers.
