# main.py
# Objective: Summarize a given piece of text as part of a simple pipeline.

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def run_summarization_pipeline():
    """
    Creates a prompt template for summarization, uses an LLMChain, and prints the summary.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    # Define the prompt template for summarization
    prompt_template = "Summarize the following article:\n\n{article}\n\nSummary:"
    prompt = PromptTemplate(template=prompt_template, input_variables=["article"])

    # Create an LLMChain
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    # Article to be summarized
    article_text = """The Amazon rainforest is the largest rainforest in the world, covering an area of over 5.5 million square kilometers. It is home to an incredible diversity of plant and animal life, including many species that are found nowhere else on Earth. The rainforest plays a crucial role in regulating the Earth's climate by absorbing vast amounts of carbon dioxide. However, it is currently facing significant threats from deforestation, logging, and climate change, which are leading to habitat loss and increased carbon emissions."""

    # Run the summarization chain
    summary = llm_chain.invoke({"article": article_text})
    print(summary["text"])

if __name__ == "__main__":
    run_summarization_pipeline()
