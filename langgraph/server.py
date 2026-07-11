from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
from typing import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.3
)

class SoftwareTeamState(TypedDict):
    problem_statement: str
    project_plan: str
    requirements: str
    architecture: str
    development: str
    review: str
    documentation: str

def planner(state: SoftwareTeamState):
    prompt = f"""You are an Expert Project Planner. Create for this problem:
{state["problem_statement"]}
1. Project Goal 2. Main Modules 3. Workflow 4. Deliverables"""
    response = llm.invoke(prompt)
    state["project_plan"] = response.content
    return state

def requirement_analyst(state: SoftwareTeamState):
    prompt = f"""You are a Senior Business Analyst. Generate requirements for:
{state["project_plan"]}
1. Functional Requirements 2. Non Functional Requirements 3. Actors 4. Main Features"""
    response = llm.invoke(prompt)
    state["requirements"] = response.content
    return state

def architect(state: SoftwareTeamState):
    prompt = f"""You are a Software Architect. Suggest tech stack for:
{state["requirements"]}
Frontend, Backend, Database, Authentication, Deployment, Folder Structure"""
    response = llm.invoke(prompt)
    state["architecture"] = response.content
    return state

def developer(state: SoftwareTeamState):
    prompt = f"""You are a Senior Developer. Generate development plan for:
Plan: {state["project_plan"]}
Reqs: {state["requirements"]}
Arch: {state["architecture"]}
1. Folder Structure 2. Database Tables 3. REST APIs 4. Steps 5. Best Practices"""
    response = llm.invoke(prompt)
    state["development"] = response.content
    return state

def reviewer(state: SoftwareTeamState):
    prompt = f"""You are a Code Reviewer. Review this plan:
{state["development"]}
1. Strengths 2. Weaknesses 3. Security 4. Performance 5. Deployment"""
    response = llm.invoke(prompt)
    state["review"] = response.content
    return state

def documentation(state: SoftwareTeamState):
    prompt = f"""You are a Technical Writer. Create docs for:
Plan: {state["project_plan"]}
Reqs: {state["requirements"]}
Arch: {state["architecture"]}
Dev: {state["development"]}
Review: {state["review"]}
1. Overview 2. Tech Stack 3. Folder Structure 4. Modules 5. Installation 6. Future"""
    response = llm.invoke(prompt)
    state["documentation"] = response.content
    return state

graph = StateGraph(SoftwareTeamState)
graph.add_node("Planner", planner)
graph.add_node("Requirements", requirement_analyst)
graph.add_node("Architecture", architect)
graph.add_node("Developer", developer)
graph.add_node("Reviewer", reviewer)
graph.add_node("Documentation", documentation)
graph.add_edge(START, "Planner")
graph.add_edge("Planner", "Requirements")
graph.add_edge("Requirements", "Architecture")
graph.add_edge("Architecture", "Developer")
graph.add_edge("Developer", "Reviewer")
graph.add_edge("Reviewer", "Documentation")
graph.add_edge("Documentation", END)
workflow = graph.compile()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    problem = data.get('problem_statement', '')
    
    if not problem.strip():
        return jsonify({'error': 'Please enter a problem statement'}), 400
    
    initial_state = {
        "problem_statement": problem,
        "project_plan": "",
        "requirements": "",
        "architecture": "",
        "development": "",
        "review": "",
        "documentation": ""
    }
    
    result = workflow.invoke(initial_state)
    
    return jsonify({
        'project_plan': result['project_plan'],
        'requirements': result['requirements'],
        'architecture': result['architecture'],
        'development': result['development'],
        'review': result['review'],
        'documentation': result['documentation']
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
