# Basic LangGraph Agent
#
# This script demonstrates a basic LangGraph agent with a simple graph.
# The graph has two nodes and transitions between them based on a condition.

import os
from dotenv import load_dotenv
from langgraph.graph import Graph

load_dotenv()

# Define the state
class AgentState:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def is_max(self):
        return self.value >= 5

# Define the nodes
def node_a(state):
    print("Node A")
    state.increment()
    return {"state": state}

def node_b(state):
    print("Node B")
    state.increment()
    return {"state": state}

# Define the graph
workflow = Graph()
workflow.add_node("A", node_a)
workflow.add_node("B", node_b)

# Define the edges
workflow.add_edge("A", "B")
workflow.add_edge("B", "A")

# Set the entry point
workflow.set_entry_point("A")

# Compile the graph
app = workflow.compile()

# Run the graph
state = AgentState()
for s in app.stream({}, {"recursion_limit": 10}):
    if s["__end__"]:
        break
    print(s)
    state.increment()
    if state.is_max():
        break
