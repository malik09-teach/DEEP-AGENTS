# Agent Workflow Examples

## Building a ReAct-Style Graph in LangGraph

```python
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# 1. Define Agent State
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# 2. Define Nodes
def agent_node(state: AgentState):
    # Call model with tool bindings
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END

# 3. Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, {
    "tools": "tools",
    END: END
})
workflow.add_edge("tools", "agent")

# 4. Compile with Checkpointer
checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)

# 5. Invoke Graph
config = {"configurable": {"thread_id": "thread-1"}}
result = app.invoke(
    {"messages": [("user", "Analyze recent sales trends")]},
    config=config
)
print(result["messages"][-1].content)
```
