"""
This script creates a LangChain agent that can read a scanned PDF invoice,
extract text from it using Optical Character Recognition (OCR), and answer
questions about its content.

**Warning:** This script requires the Tesseract OCR engine to be installed on your
system.

- For Debian/Ubuntu: `sudo apt-get install tesseract-ocr`
- For macOS (using Homebrew): `brew install tesseract`
- For Windows: Download and install from the official Tesseract repository.
  You may also need to add the Tesseract installation directory to your
  system's PATH environment variable.
"""
import os
import sys
import time
import warnings
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from pdf2image import convert_from_path
import pytesseract
# from PIL import Image

# Ignore specific warnings
warnings.filterwarnings("ignore", message="API key must be provided when using hosted LangSmith API")

# Load environment variables from .env file
load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("MODEL")

@tool
def extract_text_from_scanned_pdf(pdf_path: str) -> str:
    """
    Extracts text from a scanned PDF file using OCR.

    Args:
        pdf_path: The file path to the scanned PDF.

    Returns:
        The extracted text from the PDF.
    """
    if not os.path.exists(pdf_path):
        return f"Error: File not found at {pdf_path}"
    try:
        images = convert_from_path(pdf_path)
        extracted_text = ""
        for image in images:
            extracted_text += pytesseract.image_to_string(image) + "\n"
        return extracted_text
    except Exception as e:
        return f"An error occurred during OCR: {e}"

def run_invoice_processing_agent():
    """
    Initializes and runs an agent to process an invoice PDF.
    """
    # Check for Tesseract installation
    try:
        pytesseract.get_tesseract_version()
    except pytesseract.TesseractNotFoundError:
        print("TesseractNotFoundError: Tesseract is not installed or not in your PATH.")
        print("Please install Tesseract and try again.")
        sys.exit(1)
    
    wait_time = 15
    print(f"wait for {wait_time} seconds ...")
    for reamaining in range(wait_time, 0, -1):
        sys.stdout.write(f"\rWaiting for {reamaining} seconds...")
        sys.stdout.flush()
        time.sleep(1)
    print("\rWaiting complete!                  ")

    llm = ChatGoogleGenerativeAI(model=model, google_api_key=google_api_key)
    tools = [extract_text_from_scanned_pdf]
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    invoice_pdf_path = os.path.join(BASE_DIR, "scanned_invoice.pdf")

    # Create a dummy PDF for demonstration if it doesn't exist
    if not os.path.exists(invoice_pdf_path):
        print(f"'{invoice_pdf_path}' not found.")
        print("Please place your scanned PDF invoice in the 'project_08_simple_data_retrieval_agent' directory.")
        # As creating a real scanned PDF is complex, we will exit.
        # In a real scenario, you would have the invoice ready.
        return

    print(f"\n--- Processing Invoice: {invoice_pdf_path} ---")
    response = agent_executor.invoke({
        "input": f"Please extract the total amount due from the invoice located at '{invoice_pdf_path}'."
    })

    print("\n\n--- FINAL AGENT ANSWER ---")
    print(response['output'])

if __name__ == "__main__":
    run_invoice_processing_agent()