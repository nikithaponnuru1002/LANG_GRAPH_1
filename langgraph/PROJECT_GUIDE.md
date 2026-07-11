# AI Software Team - Complete Beginner's Guide

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [The Big Idea (Moto)](#2-the-big-idea)
3. [How It Works - Simple Analogy](#3-how-it-works)
4. [Project Structure](#4-project-structure)
5. [Key Technologies](#5-key-technologies)
6. [The 6 AI Agents Explained](#6-the-6-ai-agents)
7. [LangGraph - The Brain](#7-langgraph---the-brain)
8. [Flow Diagram](#8-flow-diagram)
9. [How to Run](#9-how-to-run)
10. [Code Walkthrough](#10-code-walkthrough)
11. [Key Concepts for Beginners](#11-key-concepts)

---

## 1. Project Overview

**What is this project?**

This project is an **AI-powered virtual software team**. You give it a problem (like "Build an e-commerce website"), and 6 AI agents work **one after another** to produce a complete project plan, including:

- Project goals and modules
- Functional & non-functional requirements
- Technology stack (frontend, backend, database)
- Development steps and folder structure
- Code review with strengths & weaknesses
- Full technical documentation

**In one sentence:** It turns a single problem statement into a full software project blueprint using AI agents.

---

## 2. The Big Idea (Moto)

> **"Why have one AI do everything, when you can have a TEAM of specialized AIs?"**

In real software companies, a project goes through multiple people:
- A **Project Manager** plans it
- A **Business Analyst** writes requirements
- An **Architect** picks the tech stack
- A **Developer** builds it
- A **Reviewer** checks quality
- A **Technical Writer** documents it

This project **simulates that entire team using AI agents**, where each agent is an expert at ONE job, and they pass their work to the next agent like a relay race.

---

## 3. How It Works - Simple Analogy

Think of it like a **factory assembly line**:

```
 INPUT                    ASSEMBLY LINE                        OUTPUT
                                                          
[Your Problem] --> [Planner] --> [Analyst] --> [Architect] --> [Developer] --> [Reviewer] --> [Docs] --> [Final Plan]
 "Build an           |              |              |               |              |            |
  e-commerce     Creates        Picks tech     Writes code    Reviews &     Creates
  website"       goals &        stack          plan & APIs    improves      full docs
                 modules                                             it
```

Each agent:
1. **Reads** what the previous agent produced
2. **Thinks** about it (using AI/LLM)
3. **Writes** its own output
4. **Passes** it to the next agent

The **output of one agent becomes the input of the next**. This is called a "chain" or "pipeline."

---

## 4. Project Structure

```
langgraph/
|
|-- .env                    # Secret API key (Groq API key)
|-- app.py                  # CLI version (runs in terminal)
|-- server.py               # Web server version (Flask + frontend)
|-- requirements.txt        # Python packages needed
|-- PLAN.txt                # Development plan/notes
|
|-- static/                 # Frontend files
|   |-- index.html          # Main web page
|   |-- style.css           # Styling (dark theme, cards, animations)
|   |-- app.js              # JavaScript (API calls, UI logic)
|
|-- PROJECT_GUIDE.md        # This file!
```

---

## 5. Key Technologies

| Technology | What It Does | Why It's Used |
|---|---|---|
| **LangGraph** | Creates AI workflows as graphs | Connects 6 agents in a chain/pipeline |
| **LangChain** | Framework for working with LLMs | Provides tools to interact with AI models |
| **Groq (Llama 3.3)** | The actual AI model (LLM) | Powers all 6 agents - the "brain" |
| **Flask** | Web server framework | Serves the frontend and handles API requests |
| **Python-dotenv** | Loads `.env` files | Keeps the API key secure and out of code |
| **HTML/CSS/JS** | Frontend interface | Lets users type problems and see results |

---

## 6. The 6 AI Agents Explained

Each agent is a **function** in the code that:
- Receives the current state (all work done so far)
- Sends a prompt to the AI model
- Saves its output back to the state

### Agent 1: Planner
- **Role:** Expert Project Planner
- **Input:** Your problem statement
- **Output:** Project goal, main modules, workflow, deliverables
- **Think of as:** The Project Manager

### Agent 2: Requirements Analyst
- **Role:** Senior Business Analyst
- **Input:** Project plan from Planner
- **Output:** Functional requirements, non-functional requirements, actors, main features
- **Think of as:** The Business Analyst

### Agent 3: Architect
- **Role:** Software Architect
- **Input:** Requirements from Analyst
- **Output:** Frontend choice, Backend choice, Database, Auth, Deployment strategy, Folder structure
- **Think of as:** The System Architect

### Agent 4: Developer
- **Role:** Senior Software Developer
- **Input:** Plan + Requirements + Architecture
- **Output:** Folder structure, Database tables, REST APIs, Development steps, Best practices
- **Think of as:** The Lead Developer

### Agent 5: Reviewer
- **Role:** Senior Code Reviewer
- **Input:** Development plan from Developer
- **Output:** Strengths, Weaknesses, Security improvements, Performance improvements, Deployment suggestions
- **Think of as:** The QA / Code Reviewer

### Agent 6: Documentation
- **Role:** Technical Documentation Writer
- **Input:** ALL previous outputs (plan, requirements, architecture, development, review)
- **Output:** Project overview, Tech stack summary, Folder structure, Modules, Installation steps, Future enhancements
- **Think of as:** The Technical Writer

---

## 7. LangGraph - The Brain

### What is LangGraph?

LangGraph is a library that lets you create **AI workflows as graphs**. Think of a graph like a flowchart:

- **Nodes** = Steps/Agents (each agent is a node)
- **Edges** = Connections (which agent connects to which)
- **State** = A shared bag of data that all agents read from and write to

### How it's used in this project:

```python
# 1. Define what data the state holds
class SoftwareTeamState(TypedDict):
    problem_statement: str    # Your input
    project_plan: str         # Planner's output
    requirements: str         # Analyst's output
    architecture: str         # Architect's output
    development: str          # Developer's output
    review: str               # Reviewer's output
    documentation: str        # Documentation's output

# 2. Create the graph
graph = StateGraph(SoftwareTeamState)

# 3. Add agents as nodes
graph.add_node("Planner", planner)
graph.add_node("Requirements", requirement_analyst)
graph.add_node("Architecture", architect)
graph.add_node("Developer", developer)
graph.add_node("Reviewer", reviewer)
graph.add_node("Documentation", documentation)

# 4. Connect them with edges (the order they run)
graph.add_edge(START, "Planner")              # Start -> Planner
graph.add_edge("Planner", "Requirements")     # Planner -> Requirements
graph.add_edge("Requirements", "Architecture")# Requirements -> Architecture
graph.add_edge("Architecture", "Developer")   # Architecture -> Developer
graph.add_edge("Developer", "Reviewer")       # Developer -> Reviewer
graph.add_edge("Reviewer", "Documentation")   # Reviewer -> Documentation
graph.add_edge("Documentation", END)          # Documentation -> End

# 5. Compile and run
app = graph.compile()
result = app.invoke(initial_state)
```

### The State (Shared Data Bag)

The `SoftwareTeamState` is like a shared whiteboard:

```
initial_state = {
    "problem_statement": "Build an e-commerce website",  <-- YOU write this
    "project_plan": "",      <-- Empty, Planner fills it
    "requirements": "",      <-- Empty, Analyst fills it
    "architecture": "",      <-- Empty, Architect fills it
    "development": "",       <-- Empty, Developer fills it
    "review": "",            <-- Empty, Reviewer fills it
    "documentation": ""     <-- Empty, Documentation fills it
}
```

After the workflow runs:
```
result = {
    "problem_statement": "Build an e-commerce website",
    "project_plan": "## Project Goal\n...",       <-- FILLED
    "requirements": "## Functional Requirements\n...",  <-- FILLED
    "architecture": "## Frontend: React\n...",    <-- FILLED
    "development": "## Folder Structure\n...",    <-- FILLED
    "review": "## Strengths\n...",                <-- FILLED
    "documentation": "## Project Overview\n..."  <-- FILLED
}
```

---

## 8. Flow Diagram

```
                    +-----------+
                    |   START   |
                    +-----+-----+
                          |
                          v
                +-------------------+
                |     PLANNER       |
                |  (Project Goals,  |
                |   Modules, etc.)  |
                +--------+----------+
                         |
                         v
              +---------------------+
              | REQUIREMENTS ANALYST|
              | (Functional/Non-    |
              |  Functional Reqs)   |
              +--------+------------+
                       |
                       v
              +---------------------+
              |     ARCHITECT       |
              | (Tech Stack:        |
              |  Frontend, Backend, |
              |  DB, Auth, Deploy)  |
              +--------+------------+
                       |
                       v
              +---------------------+
              |     DEVELOPER       |
              | (Folder Structure,  |
              |  APIs, DB Tables,   |
              |  Dev Steps)         |
              +--------+------------+
                       |
                       v
              +---------------------+
              |     REVIEWER        |
              | (Strengths,         |
              |  Weaknesses,        |
              |  Security, Perf)    |
              +--------+------------+
                       |
                       v
              +---------------------+
              |   DOCUMENTATION     |
              | (Overview, Tech     |
              |  Stack, Modules,    |
              |  Installation)      |
              +--------+------------+
                       |
                       v
                    +-----+
                    | END |
                    +-----+
```

---

## 9. How to Run

### Option A: Terminal Version (app.py)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your Groq API key to .env file
#    (already done - GROQ_API_KEY=your_key_here)

# 3. Run
python app.py

# 4. Type your problem statement when prompted
# 5. Wait for all 6 agents to process
# 6. See the full output in terminal
```

### Option B: Web Version (server.py)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
python server.py

# 3. Open browser: http://localhost:5000
# 4. Type your problem statement
# 5. Click "Generate Plan"
# 6. See results in expandable cards
```

---

## 10. Code Walkthrough

### How Each Agent Function Works (app.py:54-84)

```python
def planner(state: SoftwareTeamState):
    # 1. Build a prompt with the problem statement
    prompt = f"""
    You are an Expert Project Planner.
    Problem Statement: {state["problem_statement"]}
    Create: 1. Project Goal 2. Main Modules 3. Workflow 4. Deliverables
    """

    # 2. Send prompt to the AI model (Groq Llama 3.3)
    response = llm.invoke(prompt)

    # 3. Save the AI's response into the state
    state["project_plan"] = response.content

    # 4. Return the updated state
    return state
```

Every agent follows the same pattern:
1. Read from state
2. Build a prompt
3. Call the LLM
4. Save result to state
5. Return state

### How the Web Server Works (server.py:107-134)

```python
@app.route('/generate', methods=['POST'])
def generate():
    # 1. Get problem statement from frontend
    problem = request.json.get('problem_statement', '')

    # 2. Create initial state
    initial_state = { "problem_statement": problem, ... }

    # 3. Run the entire LangGraph workflow
    result = workflow.invoke(initial_state)

    # 4. Return JSON to frontend
    return jsonify({
        'project_plan': result['project_plan'],
        'requirements': result['requirements'],
        ...
    })
```

### How the Frontend Works (static/app.js)

```javascript
async function generatePlan() {
    // 1. Get text from textarea
    const problem = input.value.trim();

    // 2. Send POST request to /generate
    const response = await fetch('/generate', {
        method: 'POST',
        body: JSON.stringify({ problem_statement: problem })
    });

    // 3. Get JSON response
    const data = await response.json();

    // 4. Put each section into its card
    document.getElementById('projectPlan').textContent = data.project_plan;
    document.getElementById('requirements').textContent = data.requirements;
    // ... etc
}
```

---

## 11. Key Concepts for Beginners

### What is an LLM?
**LLM = Large Language Model** (like ChatGPT, Llama, etc.)
It's an AI that takes text input and produces text output. In this project, we use **Llama 3.3 70B** through **Groq** (a fast LLM hosting service).

### What is LangChain?
LangChain is a Python library that makes it easy to work with LLMs. It provides:
- Standard ways to call different AI models
- Tools to build prompts
- Utilities for chaining operations

### What is LangGraph?
LangGraph extends LangChain to create **graph-based workflows**. Instead of a simple chain (A -> B -> C), you can create complex graphs with branches, loops, and conditions.

### What is a State Graph?
A State Graph is a specific type of LangGraph workflow where:
- There is a **shared state** (data dictionary) that flows through the graph
- Each **node** (agent) reads from and writes to this state
- The state carries all the information from start to finish

### What is Groq?
Groq is a company that provides **extremely fast** access to AI models. They host the Llama 3.3 model, and we access it via an API key.

### What is Flask?
Flask is a lightweight Python web framework. It:
- Serves the frontend HTML/CSS/JS files
- Handles the `/generate` API endpoint
- Connects the frontend to the LangGraph backend

### What is the `.env` file?
The `.env` file stores **secret information** (like API keys) that should NOT be in your code. It's loaded by `python-dotenv` so you can access it with `os.getenv("GROQ_API_KEY")`.

### What is a TypedDict?
`TypedDict` is a Python feature that lets you define a dictionary with specific keys and value types. It's like a simple class but works as a dictionary:

```python
class SoftwareTeamState(TypedDict):
    problem_statement: str   # Must be a string
    project_plan: str        # Must be a string
    # ...
```

---

## Quick Reference

| Term | Meaning |
|---|---|
| **Node** | An agent/function in the graph |
| **Edge** | A connection between two nodes |
| **State** | Shared data dictionary passed through the graph |
| **LLM** | Large Language Model (the AI brain) |
| **Prompt** | The instruction/question sent to the AI |
| **Invoke** | Call the AI model with a prompt |
| **Compile** | Convert the graph definition into a runnable app |
| **Endpoint** | A URL the server responds to (e.g., `/generate`) |
| **CORS** | Cross-Origin Resource Sharing (allows frontend to call backend) |

---

*This guide covers the complete project. For questions, refer to the code comments in app.py and server.py.*
