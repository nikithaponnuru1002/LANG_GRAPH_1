import os
from typing import TypedDict

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

# ==========================================================
# Load Groq LLM
# ==========================================================

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.3
)

print("\nGroq LLM Loaded Successfully!")

# ==========================================================
# LangGraph State
# ==========================================================

class SoftwareTeamState(TypedDict):

    problem_statement: str

    project_plan: str

    requirements: str

    architecture: str

    development: str

    review: str

    documentation: str

# ==========================================================
# Planner Node
# ==========================================================

def planner(state: SoftwareTeamState):

    print("\nPlanner Agent Running...")

    prompt = f"""
You are an Expert Project Planner.

Problem Statement:

{state["problem_statement"]}

Create

1. Project Goal

2. Main Modules

3. Workflow

4. Deliverables

Return professional output.
"""

    response = llm.invoke(prompt)

    state["project_plan"] = response.content

    print("Planner Completed.")

    return state

# ==========================================================
# Requirement Analyst Node
# ==========================================================

def requirement_analyst(state: SoftwareTeamState):

    print("\nRequirement Analyst Running...")

    prompt = f"""
You are a Senior Business Analyst.

Project Plan

{state["project_plan"]}

Generate

Functional Requirements

Non Functional Requirements

Actors

Main Features

Professional Output.
"""

    response = llm.invoke(prompt)

    state["requirements"] = response.content

    print("Requirements Completed.")

    return state

# ==========================================================
# Architecture Node
# ==========================================================

def architect(state: SoftwareTeamState):

    print("\nArchitect Agent Running...")

    prompt = f"""
You are a Software Architect.

Requirements

{state["requirements"]}

Suggest

Frontend

Backend

Database

Authentication

Deployment

Folder Structure

Explain why each technology is selected.
"""

    response = llm.invoke(prompt)

    state["architecture"] = response.content

    print("Architecture Completed.")

    return state

# ==========================================================
# Build Graph
# ==========================================================

graph = StateGraph(SoftwareTeamState)

graph.add_node("Planner", planner)

graph.add_node("Requirements", requirement_analyst)

graph.add_node("Architecture", architect)

graph.add_edge(START, "Planner")

graph.add_edge("Planner", "Requirements")

graph.add_edge("Requirements", "Architecture")

# END will be connected in Part 2

print("\nGraph Created Successfully!")
# ==========================================================
# Developer Node
# ==========================================================

def developer(state: SoftwareTeamState):

    print("\nDeveloper Agent Running...")

    prompt = f"""
You are a Senior Software Developer.

Project Plan

{state["project_plan"]}

Requirements

{state["requirements"]}

Architecture

{state["architecture"]}

Generate

1. Folder Structure

2. Database Tables

3. REST APIs

4. Development Steps

5. Best Practices

Return professional output.
"""

    response = llm.invoke(prompt)

    state["development"] = response.content

    print("Development Completed.")

    return state


# ==========================================================
# Reviewer Node
# ==========================================================

def reviewer(state: SoftwareTeamState):

    print("\nReviewer Agent Running...")

    prompt = f"""
You are a Senior Code Reviewer.

Review the proposed software development plan.

Development

{state["development"]}

Provide

1. Strengths

2. Weaknesses

3. Security Improvements

4. Performance Improvements

5. Deployment Suggestions

Return professional output.
"""

    response = llm.invoke(prompt)

    state["review"] = response.content

    print("Review Completed.")

    return state


# ==========================================================
# Documentation Node
# ==========================================================

def documentation(state: SoftwareTeamState):

    print("\nDocumentation Agent Running...")

    prompt = f"""
You are a Technical Documentation Writer.

Using the following information

Project Plan

{state["project_plan"]}

Requirements

{state["requirements"]}

Architecture

{state["architecture"]}

Development

{state["development"]}

Review

{state["review"]}

Generate

1. Project Overview

2. Technology Stack

3. Folder Structure

4. Modules

5. Installation Steps

6. Future Enhancements

Return professional documentation.
"""

    response = llm.invoke(prompt)

    state["documentation"] = response.content

    print("Documentation Completed.")

    return state


# ==========================================================
# Add Remaining Nodes
# ==========================================================

graph.add_node("Developer", developer)

graph.add_node("Reviewer", reviewer)

graph.add_node("Documentation", documentation)


# ==========================================================
# Add Remaining Edges
# ==========================================================

graph.add_edge("Architecture", "Developer")

graph.add_edge("Developer", "Reviewer")

graph.add_edge("Reviewer", "Documentation")

graph.add_edge("Documentation", END)


# ==========================================================
# Compile Graph
# ==========================================================

app = graph.compile()

print("\nGraph Compiled Successfully!")


# ==========================================================
# User Input
# ==========================================================

problem = input("\nEnter Problem Statement:\n\n")


# ==========================================================
# Initial State
# ==========================================================

initial_state = {

    "problem_statement": problem,

    "project_plan": "",

    "requirements": "",

    "architecture": "",

    "development": "",

    "review": "",

    "documentation": ""

}


# ==========================================================
# Execute Graph
# ==========================================================

print("\nExecuting LangGraph Workflow...\n")

result = app.invoke(initial_state)


# ==========================================================
# Final Output
# ==========================================================

print("\n" + "=" * 80)
print("PROJECT PLAN")
print("=" * 80)
print(result["project_plan"])

print("\n" + "=" * 80)
print("REQUIREMENTS")
print("=" * 80)
print(result["requirements"])

print("\n" + "=" * 80)
print("ARCHITECTURE")
print("=" * 80)
print(result["architecture"])

print("\n" + "=" * 80)
print("DEVELOPMENT")
print("=" * 80)
print(result["development"])

print("\n" + "=" * 80)
print("REVIEW")
print("=" * 80)
print(result["review"])

print("\n" + "=" * 80)
print("DOCUMENTATION")
print("=" * 80)
print(result["documentation"])

print("\nWorkflow Completed Successfully!")