from typing import TypedDict, List

class GraphState(TypedDict):
    """
    Represents the state of our graph.
`
    Attributes:
        question: User question
        improved_question: Improved user question by the system
        reasoning_for_improved_question: Reasoning behind the improved question
        field_of_expertise: Field of assistant expertise required to answer the question
        context: Documentation extracted from knowledge base
        solution: Code solution to answer user question
        errors: List of error messages generated during code evaluation
        static_analysis_results: Result of static analysis on the generated code
        iterations: Number of attempts to generate the solution
        llm_name: Name of the model to be used to answer the question
        api_key: API key for the model
    """

    question: str
    improved_question: str
    reasoning_for_improved_question: str
    field_of_expertise: str
    context: str
    solution: str
    errors: List[str]
    static_analysis_results: str
    iterations: int
    llm_name: str
    api_key: str

    
