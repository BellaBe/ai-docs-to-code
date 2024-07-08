from typing import Any, Dict
from graph.entities import GraphState
from graph.chains.code_generator import CodeGenerationChain

def generate_code(state: GraphState) -> Dict[str, Any]:
    """
    Generate a code solution

    Args:
        state (GraphState): The current graph state

    Returns:
        dict: New key added to state, generation
    """
    print("<----GENERATING CODE SOLUTION----")

    context = state["context"]
    field_of_expertise = state["field_of_expertise"]
    llm_name = state["llm_name"]
    api_key = state["api_key"]
    
    generation_chain = CodeGenerationChain(api_key, llm_name)
    
    code_solution = generation_chain.invoke(
        {"context": context, "question": state["improved_question"], "field_of_expertise": field_of_expertise}
    )
    print("----GENERATING CODE SOLUTION---->")
    
    state["generation"] = code_solution
    return state

