from graph.state import GraphState


max_iterations = 3
# Reflect
# flag = 'reflect'
flag = "do not reflect"


def decide_to_finish(state: GraphState):
    """
    Determines whether to finish.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    error = state["error"]
    iterations = state["iterations"]

    if error == "no" or iterations == max_iterations:
        print("---DECISION: FINISH---")
        return "end"
    else:
        print("---DECISION: RE-TRY SOLUTION---")
        if flag == "reflect":
            return "reflect"
        else:
            return "generate"
            
def decide_to_generate(state: GraphState):
    """
    Determines whether to transform query, websearch or generate code.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    
    web_search = state["web_search"]

    if web_search == True:
        print("---DECISION: WEBSEARCH---")
        return "websearch"
    else:
        print("---DECISION: GENERATE---")
        return "generate"