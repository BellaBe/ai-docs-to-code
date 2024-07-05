from typing import Any, Dict

from graph.entities import GraphState
from graph.chains.generation import generation_chain

    
def generate(state: GraphState):
    """
    Generate a code solution

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation
    """

    print("---GENERATING CODE SOLUTION---")


    context = state["context"]
    field_of_expertise = state["field_of_expertise"]
    
    flattened_context = [doc.page_content + "\n" for doc in context]
    

    code_solution = generation_chain.invoke(
        {"context": context, "question": state["improved_question"], "field_of_expertise": field_of_expertise}
    )
    return {"generation": code_solution}