from typing import Any, Dict
from graph.state import GraphState
from graph.chains.question_rewriter import question_rewriter


def transform_query(state: GraphState):
    """
    Transforms original query of the user into a better query.
    
    Args:
        state(dict): The current state of the graph.
    
    Returns:
        state(dict): Filtered our irrelevant documents and updated web_search flag.
    """
    print("<----TRANSFORM QUERY----")
    
    question = state["question"]
    field_of_expertise = state["field_of_expertise"]
    result = question_rewriter.invoke({"question": question, "field_of_expertise": field_of_expertise})
    
    print("Improved Question: ", result)
    
    print("----TRANSFORM QUERY---->")
    
    return {"improved_question": result}
    
    