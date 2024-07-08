from typing import Any, Dict

from graph.entities import GraphState
from graph.chains.reflector import ReflectorChain

def reflect(state: GraphState) -> Dict[str, Any]:
    """
    Reflect on errors

    Args:
        state (GraphState): The current graph state

    Returns:
        state (dict): New keys added to state, improved_question and reflection
    """

    print("---REFLECTING ON ANSWERS---")

    question = state["improved_question"]
    code_solution = state["generation"]
    is_answer_useful = state["is_answer_useful"]
    answer_reasoning = state["answer_reasoning"]
    expertise_field = state["field_of_expertise"]
    api_key = state["api_key"]
    llm_name = state["llm_name"]
    
    reflector = ReflectorChain(api_key, llm_name)
    
    result = reflector.invoke({
        "question": question,
        "improved_question": question,
        "generation": code_solution,
        "is_answer_useful": is_answer_useful,
        "answer_reasoning": answer_reasoning,
        "field_of_expertise": expertise_field
    })
    
    print("RESULT REFLECT", result)
    print("STATE", state)

    state["improved_question"] = result.improved_question
    state["reflection"] = result.reflections

    return state