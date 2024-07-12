from graph.entities import GraphState


max_iterations = 3


def decide_to_finish(state: GraphState) -> str:
    """
    Determines whether to finish.

    Args:
        state (GraphState): The current graph state

    Returns:
        str: Next node to call
    """

    iterations = state.get("iterations")

        
    if iterations >= max_iterations:
        print("STATE: ", state)
        print("---DECISION: FINISH, MAX ITERATIONS REACHED---")
        return "end"
        
    if len(state["errors"]) == 0:
        print("---DECISION: FINISH, NO ERRORS---")
        return "end"

    print("---DECISION: RE-TRY SOLUTION---")
    return "fix_code"
    