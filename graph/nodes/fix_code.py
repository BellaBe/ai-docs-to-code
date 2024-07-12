from typing import Any, Dict
from graph.entities import GraphState
from graph.chains.code_fixer import CodeFixerChain

def fix_code(state: GraphState) -> GraphState:
    """
    Fix the code solution

    Args:
        state (GraphState): The current graph state

    Returns:
        state (GraphState): Updated state with the fixed solution
    """
    
    print("<---FIXING CODE SOLUTION---")
    
    # Extract necessary information from the state
    question = state["improved_question"]
    field_of_expertise = state["field_of_expertise"]
    solution = state["solution"]
    context = state["context"]
    errors = state.get("errors", [])
    
    api_key = state["api_key"]
    llm_name = state["llm_name"]
    
    # Initialize CodeFixerChain
    code_fixer = CodeFixerChain(api_key, llm_name)
    
    # Prepare input data for code fixer
    input_data = {
        "question": question,
        "field_of_expertise": field_of_expertise,
        "solution": solution,
        "context": context,
        "errors": errors[-1] if errors else "No specific errors provided."
    }
    
    # Invoke the CodeFixerChain
    code_solution = code_fixer.invoke(input_data)
    
    # Update the state with the fixed solution and increment iterations
    state["iterations"] = state.get("iterations", 0) + 1
    state["solution"] = code_solution

    print("----FIXING CODE SOLUTION---->")
    
    return state
