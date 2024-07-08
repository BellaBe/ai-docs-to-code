from graph.entities import GraphState

def clean_code_block(code_block: str) -> str:
    """
    Clean the code block by removing any surrounding triple backticks.
    
    Args:
        code_block (str): The raw code block generated by the LLM.
    
    Returns:
        str: The cleaned code block.
    """
    if code_block.startswith("```") and code_block.endswith("```"):
        return code_block[3:-3].strip()
    return code_block

def evaluate_code(state: GraphState) -> GraphState:
    """
    Check code

    Args:
        state (GraphState): The current graph state

    Returns:
        GraphState: Updated state with new key added to state, error_messages if any errors occurred.
    """

    print("<----EVALUATING CODE---->")

    # State
    code_solution = state.get("generation")

    # Ensure error_messages is initialized
    if state.get("error_messages") is None:
        state["error_messages"] = ""

    if not code_solution:
        state["error_messages"] += "\nNo code solution found in the state."
        print("----EVALUATING CODE: NO CODE SOLUTION----")
        return state

    # Get solution components
    imports = getattr(code_solution, "imports", "")
    code = getattr(code_solution, "code", "")

    # Clean code block
    imports = clean_code_block(imports)
    code = clean_code_block(code)
    
    if imports == "":
        state["error_messages"] += "\nGenerated imports are empty."
        print("----EVALUATING CODE: IMPORTS BLOCK IS EMPTY----")
        return state

    if code == "":
        state["error_messages"] += "\nGenerated code is empty."
        print("----EVALUATING CODE: CODE BLOCK IS EMPTY----")
        return state

    # Check imports
    try:
        exec(imports)
    except Exception as e:
        print("----EVALUATING CODE: IMPORTS FAILED----")
        state["error_messages"] += f"\nImports failed with error: {str(e)}"
        print("----EVALUATING CODE---->")
        return state

    # Check execution
    try:
        exec(imports + "\n" + code)
    except Exception as e:
        print("----EVALUATING CODE: CODE BLOCK FAILED----")
        state["error_messages"] += f"\nCode block failed with error: {str(e)}"
        print("----EVALUATING CODE---->")
        return state

    print("----EVALUATING CODE: SUCCESS---->")
    return state
