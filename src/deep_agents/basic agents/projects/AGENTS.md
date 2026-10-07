# Deep Agents — Project Context & Architecture

> **This file is automatically loaded when a deep agent is invoked within this project.**
> It provides essential context about the codebase, architecture, conventions, and available backends.

---

## 1. Project Overview

| Field            | Value                                          |
|------------------|-------------------------------------------------|
| **Name**         | `deep-agents`                                   |
| **Version**      | `0.1.0`                                         |
| **Author**       | `malik09-teach` (xyz)   |
| **Python**       | `>=3.14`                                        |
| **Build System** | `uv_build`                                      |
| **Entry Point**  | `deep-agents = "deep_agents:main"`              |
| **Repository**   | `malik09-teach/DEEP-AGENTS`                     |

**Deep Agents** is a multi-backend AI agent framework built on top of the [deepagents](https://pypi.org/project/deepagents/) SDK, **LangChain**, and **LangGraph**. It enables the creation of autonomous, tool-using agents that can read/write files, execute shell commands, search the web, manage conversations with persistent memory, and orchestrate sub-agents — all through a unified `create_deep_agent()` API.

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USER / CLIENT                          │
│              (Notebook / Script / API Endpoint)             │
└────────────────────────┬────────────────────────────────────┘
                         │  invoke({ messages / user })
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   create_deep_agent()                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                 LangGraph State Machine               │  │
│  │                                                       │  │
│  │   ┌──────────┐    ┌──────────┐    ┌──────────┐       │  │
│  │   │  START   │───▶│  AGENT   │───▶│  TOOLS   │       │  │
│  │   └──────────┘    │  (LLM)   │◀───│  (exec)  │       │  │
│  │                   └─────┬────┘    └──────────┘       │  │
│  │                         │                             │  │
│  │                         ▼                             │  │
│  │                   ┌──────────┐                        │  │
│  │                   │   END    │                        │  │
│  │                   └──────────┘                        │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   BACKEND   │  │  CHECKPOINTER │  │     STORE        │   │
│  │ (State/FS/  │  │ (MemorySaver) │  │ (InMemoryStore)  │   │
│  │  Store/Hub) │  │               │  │                  │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     LLM PROVIDER                            │
│          ChatGroq  /  ChatGoogleGenAI  /  etc.              │
│          Model: "openai/gpt-oss-120b" (via Groq)            │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Core Dependencies

| Package                   | Purpose                                        |
|---------------------------|-------------------------------------------------|
| `deepagents`              | Core SDK — provides `create_deep_agent()`, backends, middleware, tools |
| `langchain`               | Foundation framework for LLM chains & agents    |
| `langchain-core`          | Core abstractions (messages, prompts, runnables) |
| `langchain-groq`          | Groq LLM provider integration                  |
| `langchain-google-genai`  | Google Gemini LLM integration                   |
| `langchain-community`     | Community tools (Tavily search, etc.)           |
| `langchain-tavily`        | Official Tavily web search integration          |
| `langchain-experimental`  | Experimental LangChain features                 |
| `langgraph`               | State-machine based agent orchestration         |
| `langgraph-sdk`           | LangGraph SDK & deployment utilities            |
| `python-dotenv`           | `.env` file loading for API keys                |
| `pdfplumber`              | PDF document parsing                            |
| `fastapi`                 | REST API framework (for serving agents)         |
| `flask`                   | Lightweight web framework                       |

---

## 4. `create_deep_agent()` — API Reference

The primary function to create an agent. Key parameters:

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model=llm,                    # Required: BaseChatModel or "provider:model" string
    tools=[...],                  # Optional: additional tools (merged with built-ins)
    system_prompt="...",          # Optional: custom system instructions
    backend=SomeBackend(),        # Optional: storage/persistence backend
    subagents=[...],              # Optional: child agents for delegation
    skills=["..."],               # Optional: named skill modules
    memory=["..."],               # Optional: memory configuration
    checkpointer=MemorySaver(),   # Optional: conversation checkpointing
    store=InMemoryStore(),        # Optional: cross-thread persistent store
    response_format=SomeSchema,   # Optional: structured output format
    debug=False,                  # Optional: enable debug logging
    name="agent-name",            # Optional: agent identifier
)
```

### Built-in Tools (always available)

| Tool          | Description                             |
|---------------|-----------------------------------------|
| `ls`          | List directory contents                 |
| `read_file`   | Read file contents                      |
| `write_file`  | Create or overwrite a file              |
| `edit_file`   | Edit an existing file in place          |
| `glob`        | Pattern-match file paths                |
| `grep`        | Search for patterns in files            |
| `execute`     | Run shell commands (requires sandbox)   |
| `task`        | Delegate work to sub-agents            |

---

## 5. Available Backends

Backends control how the agent persists state, manages files, and stores memories across invocations.

### 5.1 StateBackend (Default)

In-memory state management with conversation checkpointing via LangGraph's `MemorySaver`.

```python
from deepagents.backends import StateBackend
from langgraph.checkpoint.memory import MemorySaver

agent = create_deep_agent(
    model=llm,
    backend=StateBackend(),
)
```

**Features:**
- Thread-based conversation persistence (`thread_id`)
- Full message history within a thread
- No cross-thread memory (each thread is isolated)

**Use when:** You need simple conversation continuity within sessions.

---

### 5.2 FilesystemBackend

Enables file I/O operations on the local file system (or virtual filesystem).

```python
from deepagents.backends import FilesystemBackend

agent = create_deep_agent(
    model=llm,
    backend=FilesystemBackend(root_dir=".", virtual_mode=True),
)
```

**Parameters:**
- `root_dir` — Root directory for file operations
- `virtual_mode` — When `True`, uses an in-memory virtual FS (safe for experiments)

**Features:**
- Agent can create, read, edit, and delete files
- Sandboxed to `root_dir` to prevent unauthorized access
- Virtual mode for safe experimentation

**Use when:** Your agent needs to manage files (create todos, write code, etc.).

---

### 5.3 StoreBackend

Cross-thread persistent memory using LangGraph's `InMemoryStore`. Allows the agent to remember information across different conversation threads.

```python
from deepagents.backends import StoreBackend
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()

agent = create_deep_agent(
    model=llm,
    backend=StoreBackend(
        namespace=lambda rt: ("demo-user",),
    ),
    store=store,
)
```

**Parameters:**
- `namespace` — Function that returns a tuple identifying the storage namespace (e.g., per-user)

**Features:**
- Memories persist across threads
- Namespace-scoped for multi-user isolation
- Backed by `InMemoryStore` (can be swapped for persistent stores)

**Use when:** You need the agent to remember context across separate conversations.

---

### 5.4 ContextHubBackend

Repository-aware context management. Associates agent context with a named repository.

```python
from deepagents.backends import ContextHubBackend

agent = create_deep_agent(
    model=llm,
    backend=ContextHubBackend("my_repo_name"),
)
```

**Features:**
- Context scoped to a repository name
- File operations include context file management
- Useful for code-aware agents

**Use when:** You're building agents that operate within a specific project/repository context.

---

## 6. LLM Configuration

### Current Default Model

```python
from langchain_groq import ChatGroq

llm = ChatGroq(model="openai/gpt-oss-120b")
```

The project uses **Groq** as the inference provider with the `openai/gpt-oss-120b` model.

### Environment Variables Required

| Variable               | Purpose                        |
|------------------------|--------------------------------|
| `GROQ_API_KEY`         | Groq API authentication        |
| `TAVILY_API_KEY`       | Tavily web search API          |
| `LANGSMITH_API_KEY`    | LangSmith tracing/monitoring   |
| `LANGSMITH_PROJECT`    | LangSmith project name         |
| `LANGCHAIN_TRACING_V2` | Enable LangChain tracing       |

### Environment Setup Pattern

```python
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
```

---

## 7. Invocation Patterns

### Basic Invocation (no memory)

```python
response = agent.invoke({
    "messages": [{"role": "user", "content": "What is LangChain?"}]
})
print(response["messages"][-1].content)
```

### Thread-based Conversation (with memory)

```python
config = {"configurable": {"thread_id": "thread-1"}}

# First message
resp1 = agent.invoke(
    {"messages": [{"role": "user", "content": "My name is John."}]},
    config=config,
)

# Follow-up (agent remembers context)
resp2 = agent.invoke(
    {"messages": [{"role": "user", "content": "What is my name?"}]},
    config=config,
)
# Output: "Your name is John."
```

### With Custom System Prompt

```python
agent = create_deep_agent(
    model=llm,
    system_prompt="You are an expert at statistics and will give detailed answers."
)
```

### With External Tools (Tavily Search)

```python
from langchain_tavily import TavilySearch

tavily_tool = TavilySearch(max_results=3)

agent = create_deep_agent(
    model=llm,
    tools=[tavily_tool],
    system_prompt="""
    If the query requires up-to-date facts, use the Tavily search tool.
    For general knowledge, answer directly.
    """,
)
```

---

## 8. Project Structure

```
DEEP-AGENTS/
├── .env                          # API keys & configuration
├── .gitignore
├── .python-version               # Python 3.14+
├── README.md                     # Project overview
├── pyproject.toml                 # Build & dependency config
├── requirment.txt                # Pip requirements
├── uv.lock                       # UV lock file
│
└── src/
    └── deep_agents/
        ├── __init__.py            # Package entry point (main())
        │
        ├── PROJECTS/
        │   └── BEEM_PROJECT.HTML  # Example project output
        │
        └── basic agents/
            ├── todo.txt                      # Agent-generated file
            ├── basic tavily search.ipynb      # Web search agent
            ├── component_backend.ipynb        # StateBackend demo
            ├── context engineering.ipynb       # Custom system prompts
            ├── context file.ipynb             # ContextHubBackend demo
            ├── file system backend.ipynb      # FilesystemBackend demo
            ├── store_backend.ipynb            # StoreBackend + memory
            │
            └── projects/
                └── AGENTS.md                  # ← THIS FILE
```

---

## 9. Key Architectural Principles

1. **Backend-Agnostic Design** — Agents can switch between `StateBackend`, `FilesystemBackend`, `StoreBackend`, or `ContextHubBackend` with a single parameter change, keeping the agent logic unchanged.

2. **Tool Composition** — Built-in tools (file ops, shell exec, sub-agents) are always available. External tools (Tavily search, custom tools) are additive — they never replace built-ins.

3. **LangGraph State Machine** — Every agent is a compiled `StateGraph` with `START → AGENT → TOOLS → END` flow. The LLM decides when to call tools and when to respond.

4. **Thread Isolation** — Each `thread_id` maintains its own conversation history. Cross-thread memory requires `StoreBackend` with a shared `InMemoryStore`.

5. **Context Engineering** — System prompts are composable: `USER prompt → BASE prompt → SUFFIX`. Custom instructions are set via the `system_prompt` parameter.

6. **Tracing & Observability** — All agent invocations are traced via LangSmith when `LANGCHAIN_TRACING_V2=true`, enabling full visibility into tool calls, LLM reasoning, and token usage.

---

## 10. Development Workflow

### Running Notebooks

All experiments live in Jupyter notebooks under `src/deep_agents/basic agents/`. Each notebook follows this pattern:

1. **Import** — `create_deep_agent`, backend, LLM provider
2. **Configure** — Load `.env`, set environment variables
3. **Create Agent** — `create_deep_agent(model=..., backend=..., ...)`
4. **Invoke** — `agent.invoke({...}, config={...})`
5. **Inspect** — `response["messages"][-1].content`

### Pending Tasks (from `todo.txt`)

1. Verification
2. Collecting all files
3. Uploading

---

## 11. Conventions & Rules for Agents

When operating within this project, agents should follow these conventions:

- **Always load `.env`** before using any API keys
- **Use `thread_id`** for multi-turn conversations to maintain context
- **Prefer `virtual_mode=True`** for `FilesystemBackend` during development
- **Use structured message format**: `{"messages": [{"role": "user", "content": "..."}]}`
- **Trace all runs** via LangSmith for debugging and monitoring
- **Keep notebooks focused**: one notebook per backend/feature exploration
- **Document experiments** with markdown cells explaining the purpose and results
