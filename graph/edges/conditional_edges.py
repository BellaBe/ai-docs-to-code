from graph.entities import GraphState


max_iterations = 3
# Reflect
# flag = 'reflect'
flag = "do not reflect"


def decide_to_finish(state: GraphState) -> str:
    """
    Determines whether to finish.

    Args:
        state (GraphState): The current graph state

    Returns:
        str: Next node to call
    """
    error_messages = state.get("error_messages", "")

    if error_messages == "":
        print("---DECISION: FINISH---")
        return "end"

    print("---DECISION: RE-TRY SOLUTION---")
    return "reflect"
        
def decide_to_evaluate_code(state: GraphState):
    """
    Determines whether gathered context is enough to answer user's questions

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    
    is_answer_useful = state["is_answer_useful"]
    
    if is_answer_useful == "yes":
        print("---DECISION: EVALUATE CODE---")
        return "evaluate_code"
        
    print("---DECISION: REFLECT---")
    return "reflect"
    
    