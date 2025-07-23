import os
import sys
import warnings
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.rate_limiters import InMemoryRateLimiter
from pdf2image import convert_from_path
import pytesseract

# Suppress irrelevant warnings
warnings.filterwarnings("ignore", message="API key must be provided when using hosted LangSmith API")

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("MODEL")

@tool(description="Extract text from a scanned PDF using OCR. Provide the full file path.")
def extract_text_from_scanned_pdf(pdf_path: str) -> str:
    """Extracts all visible text from a scanned invoice PDF using Tesseract OCR."""
    if not os.path.exists(pdf_path):
        return f"Error: File not found at {pdf_path}"
    try:
        text = ""
        for image in convert_from_path(pdf_path):
            text += pytesseract.image_to_string(image) + "\n"
        return text
    except Exception as e:
        return f"An error occurred during OCR: {e}"

def run_invoice_processing_agent():
    try:
        pytesseract.get_tesseract_version()
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract not installed or not in PATH.")
        sys.exit(1)

    rate_limiter = InMemoryRateLimiter(
        requests_per_second=0.1, # Allows 1 request every 10 seconds (0.1 = 1 / 10).
        check_every_n_seconds=0.1, # It checks every 100 milliseconds whether a request can proceed.
        max_bucket_size=1) # Allows only 1 pending request at a time in memory (think of it like a buffer bucket).

    llm = init_chat_model(
        model=model,
        model_provider="google_genai",
        google_api_key=google_api_key,
        rate_limiter=rate_limiter)

    tools = [extract_text_from_scanned_pdf]
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    invoice_pdf_path = os.path.join(BASE_DIR, "scanned_invoice.pdf")

    if not os.path.exists(invoice_pdf_path):
        print(f"'{invoice_pdf_path}' not found. Place your scanned PDF there.")
        return

    print(f"\n--- Processing Invoice: {invoice_pdf_path} ---")
    response = agent_executor.invoke({
        "input": f"Please extract the total amount due from the invoice located at '{invoice_pdf_path}'."})

    print("\n--- FINAL AGENT ANSWER ---")
    print(response["output"])

if __name__ == "__main__":
    run_invoice_processing_agent()