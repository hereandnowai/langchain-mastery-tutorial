# main.py
# Objective: Generate marketing slogans for a product.

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def run_slogan_generator():
    """
    Creates a prompt template for slogan generation and uses an LLMChain to get slogans.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    # Define the prompt template for slogan generation
    prompt_template = """Generate 5 creative marketing slogans for a product with the following details:
Product Name: {product_name}
Description: {description}

Slogans:"""
    prompt = PromptTemplate(template=prompt_template, input_variables=["product_name", "description"])

    # Create an LLMChain
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    # Product details
    product_name = "EcoClean Dish Soap"
    description = "A powerful, plant-based dish soap that is tough on grease but gentle on hands and the environment."

    # Run the slogan generation chain
    slogans = llm_chain.invoke({"product_name": product_name, "description": description})
    print(slogans["text"])

if __name__ == "__main__":
    run_slogan_generator()
