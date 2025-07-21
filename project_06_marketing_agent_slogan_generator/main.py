from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pydantic.v1 import BaseModel, Field
from dotenv import load_dotenv
import os
import time
import sys
import warnings

warnings.filterwarnings("ignore", message="API key must be provided when using hosted LangSmith API")

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")

# Use a stable, generally available model
model = os.getenv("MODEL")

class SloganGeneratorInput(BaseModel):
    product_name: str = Field(description="The name of the product or company.")
    description: str = Field(description="A detailed description of the product or company for which to generate slogans.")

@tool(args_schema=SloganGeneratorInput)
def slogan_generator(product_name: str, description: str) -> str:
    """
    Generates 5 creative marketing slogans for a product given its name and description.
    """
    llm = ChatGoogleGenerativeAI(model=model, google_api_key=google_api_key)
    prompt_template = """Generate 5 creative marketing slogans for a product with the following details:
Product Name: {product_name}
Description: {description}

Slogans:"""
    prompt = PromptTemplate(template=prompt_template, input_variables=["product_name", "description"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    slogans = llm_chain.invoke({"product_name": product_name, "description": description})
    return slogans["text"]

def run_marketing_agent():
    """
    Creates and runs an agent that can use the slogan_generator tool.
    """
    llm = ChatGoogleGenerativeAI(model=model, google_api_key=google_api_key)
    tools = [slogan_generator]
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    
    # Provide a specific error message to help the agent recover from parsing errors
    custom_error_message = (
        "The tool input was not formatted correctly. "
        "Please format the Action Input as a valid JSON object with "
        "keys 'product_name' and 'description'."
    )
    
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=custom_error_message
    )

    product_name = "HERE AND NOW - The French Institute"
    description = "HERE AND NOW – The French Institute is a premier language school based in Chennai, dedicated to delivering immersive and practical French learning experiences. Blending structured linguistics with cultural engagement, their flagship “IMMERSION PROGRAM” helps professionals and students progress from A1 to B2 in just 108 days—designed using research-backed, psychologically optimized methods"

    # --- FINAL ADJUSTMENT ---
    # The 429 error is a rate limit error. Waiting before execution helps avoid this.
    # We increase the wait time to be safe.
    wait_time = 30
    print(f"Waiting for {wait_time} seconds to allow API quota to reset...")
    for i in range(wait_time, 0, -1):
        sys.stdout.write(f"\rWaiting... {i} seconds remaining. ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rDone waiting. Executing agent.\n")
    sys.stdout.flush()

    response = agent_executor.invoke({
        "input": f"Generate marketing slogans for the following product:\nProduct Name: {product_name}\nDescription: {description}"
    })
    print("\n--- AGENT RESPONSE ---")
    print(response["output"])

if __name__ == "__main__":
    run_marketing_agent()
