from typing import Any, Dict
from graph.entities import GraphState
from graph.chains.answer_grader import AnswerGraderChain

def grade_code(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the generation is grounded in the document and answers user's question.

    Args:
        state (GraphState): The current graph state

    Returns:
        str: Decision for next node to call
    """
    
    print("<---GRADING CODE SOLUTION---")
    
    question = state["improved_question"]
    field_of_expertise = state["field_of_expertise"]
    generation = state["generation"]
    api_key = state["api_key"]
    llm_name = state["llm_name"]
    
    answer_grader = AnswerGraderChain(api_key, llm_name)
    
    result = answer_grader.invoke({
        "question": question,
        "generation": generation,
        "field_of_expertise": field_of_expertise
    })
    
    print("---GRADING CODE SOLUTION--->")
    
    state["is_answer_useful"] = result.binary_score
    state["answer_reasoning"] = result.reasoning
    
    return state
