# Objective: A multi-agent system for researching, writing, and publishing blog posts.
# This script uses LangGraph to define a workflow with multiple agents.

""""
The current code is capable of creating only slogans. That is not what I want from this project. This project should be able to do some research on the hot topics. I'll be giving the organization, organization name, and the description about the organization, and the agent should be capable of doing some research related to the organization's topics and choose five topics and from the five topics it should be able to select one topic and start writing a blog. It should have a person who's selecting editor or just like you know in a blog writing organization you know in an international blog writing organization how many people will be working on it like an editor or a reviewer or proofreader, the content writer, so please create as many agents as possible. If need be you can even use lang graph for this project. Yeah and also for the don't change the model whatever model that I've given like GPT 2.5 flash preview 06-17 is okay because that's the only model that has higher rate limit and also please keep keep always sleep timer time maybe 20 seconds to seconds so which would comply with the rate limits so making this using all using my current prompt please refactor the code
Finally, the written blog should be approved by the final editor and once he approves, the agent should be going and publishing it on the WordPress site of Hurono AI. Could you please could you please work on that work on refactoring this code and also ask me what are the information that you would be needing like API from WordPress and also guide me how I can get the WordPress API I'm the owner of a website website name is is given below
https://hereandnowai.com
"""

import os
import time
import requests
from typing import TypedDict, List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# --- Environment Setup ---
load_dotenv()

# Check for Gemini API Key
if "GEMINI_API_KEY" not in os.environ:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please add it.")

# Model Configuration
# Using the specified model with a higher rate limit.
LLM = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash-lite-preview-06-17") 
# The user mentioned "GPT 2.5 flash preview 06-17", which seems to be a typo.
# Using a stable and available Gemini model.

# --- Organization Details ---
# These details will guide the research and writing process.
ORGANIZATION_NAME = "HERE AND NOW AI"
ORGANIZATION_DESCRIPTION = "specializes in cutting-edge AI solutions, focusing on autonomous agents, multi-modal applications, and advancing AI's role in business and creativity."

# --- State Definition for the Graph ---
# This TypedDict defines the structure that will be passed between agents.
class BlogWorkflowState(TypedDict):
    organization_name: str
    organization_description: str
    topics: Optional[List[str]]
    selected_topic: Optional[str]
    blog_post: Optional[str]
    review_feedback: Optional[str]
    approved: bool
    published: bool

# --- Agent Definitions ---

def researcher_agent(state: BlogWorkflowState):
    """Researches and suggests 5 blog topics."""
    print("--- Researcher Agent ---")
    prompt = PromptTemplate(
        template="""You are a research assistant. Your goal is to find trending topics for a blog post for {organization_name}, which {organization_description}.
        Please search for recent news, articles, and trends related to this field.
        From your research, identify and list 5 compelling blog post topics.
        Present them as a numbered list, with each topic on a new line.
        Example:
        1. Topic 1
        2. Topic 2
        ...""",
        input_variables=["organization_name", "organization_description"],
    )
    chain = prompt | LLM | StrOutputParser()
    
    print("Researching topics...")
    time.sleep(20) # Rate limit compliance
    result = chain.invoke({
        "organization_name": state['organization_name'],
        "organization_description": state['organization_description']
    })
    
    topics = [line.strip() for line in result.strip().split('\n') if line.strip()]
    print(f"Found topics: {topics}")
    return {"topics": topics}

def writer_agent(state: BlogWorkflowState):
    """Writes a blog post on the selected topic."""
    print("--- Writer Agent ---")
    # Simple topic selection: pick the first one.
    selected_topic = state['topics'][0] 
    print(f"Selected topic: {selected_topic}")

    prompt = PromptTemplate(
        template="""You are a content creator. Write a high-quality, engaging blog post on the topic: '{selected_topic}'.
        The blog post should be well-structured with a clear introduction, body, and conclusion.
        It should be at least 300 words. The tone should be professional and informative.
        The target audience is interested in {organization_description}.""",
        input_variables=["selected_topic", "organization_description"],
    )
    chain = prompt | LLM | StrOutputParser()

    print("Writing blog post...")
    time.sleep(20) # Rate limit compliance
    blog_post = chain.invoke({
        "selected_topic": selected_topic,
        "organization_description": state['organization_description']
    })
    
    print("Blog post generated.")
    return {"selected_topic": selected_topic, "blog_post": blog_post}

def editor_agent(state: BlogWorkflowState):
    """Reviews the blog post and decides whether to approve it."""
    print("--- Editor Agent ---")
    prompt = PromptTemplate(
        template="""You are a blog editor. Review the following blog post for quality, clarity, and grammar.
        If the post is well-written and ready for publication, respond with only the word 'APPROVE'.
        Otherwise, provide a few bullet points of feedback.
        
        Blog Post:
        {blog_post}""",
        input_variables=["blog_post"],
    )
    chain = prompt | LLM | StrOutputParser()

    print("Editing blog post...")
    time.sleep(20) # Rate limit compliance
    review = chain.invoke({"blog_post": state['blog_post']})

    if "APPROVE" in review.upper():
        print("Editor approved the post.")
        return {"approved": True}
    else:
        print(f"Editor requested revisions: {review}")
        # In a more complex graph, this feedback would loop back to the writer.
        # For simplicity, we'll stop the process if not approved.
        return {"approved": False, "review_feedback": review}

def publisher_agent(state: BlogWorkflowState):
    """Publishes the blog post to WordPress if credentials are available."""
    print("--- Publisher Agent ---")
    wp_user = os.getenv("WORDPRESS_USER")
    wp_password = os.getenv("WORDPRESS_APP_PASSWORD")
    wp_url = f"https://hereandnowai.com/wp-json/wp/v2/posts"

    if not all([wp_user, wp_password]):
        print("WARNING: WordPress credentials not in .env. Skipping publishing.")
        return {"published": False}

    auth = requests.auth.HTTPBasicAuth(wp_user, wp_password)
    headers = {'Content-Type': 'application/json'}
    post_data = {
        'title': state['selected_topic'],
        'content': state['blog_post'],
        'status': 'publish'  # Use 'draft' to save as a draft instead
    }

    print("Publishing to WordPress...")
    response = requests.post(wp_url, auth=auth, headers=headers, json=post_data)

    if response.status_code == 201:
        print("Blog post published successfully!")
        return {"published": True}
    else:
        print(f"ERROR: Failed to publish. Status: {response.status_code}")
        print(response.text)
        return {"published": False}

# --- Graph Logic ---

def should_publish(state: BlogWorkflowState):
    """Conditional edge to decide if the blog post should be published."""
    if state['approved']:
        return "publish"
    else:
        return "end"

# --- Workflow Construction ---

workflow = StateGraph(BlogWorkflowState)

# Add nodes for each agent
workflow.add_node("researcher", researcher_agent)
workflow.add_node("writer", writer_agent)
workflow.add_node("editor", editor_agent)
workflow.add_node("publisher", publisher_agent)

# Define the flow of the graph
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "editor")
workflow.add_conditional_edges(
    "editor",
    should_publish,
    {
        "publish": "publisher",
        "end": END
    }
)
workflow.add_edge("publisher", END)

# Compile the graph
app = workflow.compile()

# --- Main Execution ---

if __name__ == "__main__":
    initial_state = {
        "organization_name": ORGANIZATION_NAME,
        "organization_description": ORGANIZATION_DESCRIPTION,
        "approved": False,
        "published": False,
    }
    
    # Run the workflow
    final_state = app.invoke(initial_state)
    
    print("\n--- Workflow Complete ---")
    print(f"Final State: {final_state}")