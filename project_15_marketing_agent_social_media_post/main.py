# main.py
# Objective: Generate a social media post for a product or event.

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def run_social_media_post_generator():
    """
    Creates a prompt template for social media post generation and uses an LLMChain.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    # Define the prompt template for social media post generation
    prompt_template = """Generate a concise and engaging social media post (e.g., for Twitter or Instagram) for the following:
Product/Event Name: {name}
Description: {description}
Target Audience: {audience}

Include relevant hashtags. Post:"""
    prompt = PromptTemplate(template=prompt_template, input_variables=["name", "description", "audience"])

    # Create an LLMChain
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    # Product/Event details
    name = "Annual Tech Innovation Summit"
    description = "Join us for a day of groundbreaking discussions, workshops, and networking with industry leaders in AI, blockchain, and sustainable tech."
    audience = "Tech enthusiasts, developers, industry professionals"

    # Run the social media post generation chain
    post = llm_chain.invoke({"name": name, "description": description, "audience": audience})
    print(post["text"])

if __name__ == "__main__":
    run_social_media_post_generator()
