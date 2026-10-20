# LangGraph Skill

## Overview
Skill module for designing, constructing, and deploying stateful multi-agent workflows and cognitive graphs with LangGraph.

## Scope & Capabilities
- **Graph Architecture**: Defining `StateGraph` workflows with typed schemas (`TypedDict`).
- **Nodes & Edges**: Implementing node functions, standard edges, and conditional routing edges.
- **Persistence & Checkpointing**: Integrating checkpointers (`MemorySaver`, database stores) for thread-based conversational memory.
- **Human-in-the-Loop & Tool Calling**: Managing tool execution loops, approval gates, and time travel.

## Related Files
- `instructions.md`: Rules and standards for building reliable LangGraph applications.
- `examples/agent_workflow.md`: Comprehensive example of an agent workflow graph.
