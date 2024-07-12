from typing import Any, Dict
from graph.entities import GraphState
from graph.chains.code_generator import CodeGenerationChain

def generate_code(state: GraphState) -> GraphState:
    """
    Generate a code solution

    Args:
        state (GraphState): The current graph state

    Returns:
        state (GraphState): Updated state with the generated solution
    """
    print("<----GENERATING CODE SOLUTION----")

    # Extract necessary information from the state
    context = state["context"]
    field_of_expertise = state["field_of_expertise"]
    llm_name = state["llm_name"]
    api_key = state["api_key"]
    improved_question = state["improved_question"]

    # Initialize CodeGenerationChain
    generation_chain = CodeGenerationChain(api_key, llm_name)

    # Prepare input data for code generator
    input_data = {
        "context": context,
        "question": improved_question,
        "field_of_expertise": field_of_expertise
    }

    # Invoke the CodeGenerationChain
    code_solution = generation_chain.invoke(input_data)
    
    print("Generated code solution: =======", code_solution)

    # Update the state with the generated solution
    state["solution"] = code_solution

    print("----GENERATING CODE SOLUTION---->")

    return state
