def reflect(state: GraphState):
    """
    Reflect on errors

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation
    """

    print("---GENERATING CODE SOLUTION---")

    # State
    messages = state["messages"]
    iterations = state["iterations"]
    code_solution = state["generation"]
    context = state["context"]
    expertise_field = state["expertise_field"]

    # Prompt reflection

    # Add reflection
    reflections = code_gen_chain.invoke(
        {"context": context, "messages": messages, "expertise_field": expertise_field}
    )
    messages += [("assistant", f"Here are reflections on the error: {reflections}")]
    return {"generation": code_solution, "messages": messages, "iterations": iterations, "context": context, "expertise_field": expertise_field}