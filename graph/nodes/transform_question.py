from typing import Any, Dict
from graph.entities import GraphState
from graph.chains.question_rewriter import QuestionRewriterChain

def transform_question(state: GraphState) -> Dict[str, Any]:
    """
    Transforms original query of the user into a better query.
    
    Args:
        state (GraphState): The current state of the graph.
    
    Returns:
        Dict[str, Any]: New key added to state, improved_question
    """
    print("<----TRANSFORMING QUERY----")
    
    question = state["question"]
    field_of_expertise = state["field_of_expertise"]
    api_key = state["api_key"]
    llm_name = state["llm_name"]
    
    question_rewriter = QuestionRewriterChain(api_key, llm_name)
    
    result = question_rewriter.invoke({"question": question, "field_of_expertise": field_of_expertise})
    
    state["improved_question"] = result
    
    print("----TRANSFORMING QUERY---->")
    
    return state
