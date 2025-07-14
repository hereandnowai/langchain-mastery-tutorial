# main.py
# Objective: Summarize a given piece of text.

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def run_text_summarizer():
    """
    Creates a prompt template for summarization, uses an LLMChain, and prints the summary.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    # Define the prompt template for summarization
    prompt_template = "Summarize the following text:\n\n{text}\n\nSummary:"
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

    # Create an LLMChain
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    # Text to be summarized
    long_text = """The Roman Empire was a vast and powerful civilization that ruled over much of Europe, North Africa, and the Middle East for over 1000 years. It began as a republic in 509 BC and later became an empire under Augustus in 27 BC. The empire reached its peak in the 2nd century AD, controlling an area of over 5 million square kilometers. Its legacy includes significant contributions to law, architecture, engineering, language, and government. The Western Roman Empire collapsed in 476 AD, but the Eastern Roman (Byzantine) Empire continued for another thousand years."""

    # Run the summarization chain
    summary = llm_chain.invoke({"text": long_text})
    print(summary["text"])

if __name__ == "__main__":
    run_text_summarizer()
