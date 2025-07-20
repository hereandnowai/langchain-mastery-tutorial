from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = "gemini-1.5-flash"

def run_text_summarizer():
    """
    Creates a prompt template for summarization, uses a chain, and prints the summary.
    """
    llm = ChatGoogleGenerativeAI(model=model, google_api_key=google_api_key)

    # Define the prompt template for summarization
    prompt_template = "Summarize the following text:\n\n{text}\n\nSummary:"
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

    # Create a summarization chain using the new syntax
    chain = prompt | llm

    # Read the text to be summarized from the file
    try:
        with open("about-hereandnowai.txt", "r", encoding="utf-8") as f:
            long_text = f.read()
    except FileNotFoundError:
        print("Error: 'about-hereandnowai.txt' not found. Make sure the file exists in the 'project_04_text_summarizer' directory.")
        return

    # Run the summarization chain
    summary_output = chain.invoke({"text": long_text})
    print(summary_output.content)

if __name__ == "__main__":
    run_text_summarizer()