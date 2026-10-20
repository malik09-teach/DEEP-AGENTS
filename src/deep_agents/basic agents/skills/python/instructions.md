# Python Instructions

## Code Standards & Guidelines

1. **Typing & Documentation**
   - Provide type hints for all function signatures and return types.
   - Use docstrings (Google or NumPy format) for public classes and functions explaining parameters, returns, and raised exceptions.

2. **Error Handling & Resource Management**
   - Use context managers (`with` statements) for file handles, network connections, and database sessions.
   - Avoid bare `except:` clauses; catch explicit exception types.

3. **Performance & Memory**
   - Use generator expressions or iterators when handling large datasets to conserve memory.
   - Leverage vectorized operations with NumPy/Pandas rather than iterating over rows with `for` loops.
