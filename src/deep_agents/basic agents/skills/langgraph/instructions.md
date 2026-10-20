# LangGraph Instructions

## Guidelines for Building Graphs

1. **Explicit State Definition**
   - Always define graph state using Python `TypedDict` or Pydantic models.
   - Use `Annotated` with reducers (such as `operator.add` or `add_messages`) to manage append-only message lists.

2. **Deterministic Nodes & Clean Side Effects**
   - Keep node functions focused on transforming state or executing specific external tools.
   - Return dict patches rather than mutating state in place.

3. **Termination & Error Handling**
   - Ensure every conditional edge path has a valid route to `END` to prevent infinite loops.
   - Set maximum recursion limits (`recursion_limit`) in runtime configs for agent loops with tool calls.
