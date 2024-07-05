from typing import TypedDict

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: User question
        improved_question: Improved user question by the system
        error: Binary flag for control flow to indicate whether test error was tripped
        messages: With user question, error messages, reasoning
        generation: Code solution
        iterations: Number of tries
        context: Documentation of the library
        field_of_expertise: Field of assistant expertise 
        web_search: Flag for web search
        llm_name: Name of the LLM
        api_key: API key for the LLM
    """
    
    question: str
    improved_question: str
    error: bool
    messages: str
    generation: str
    iterations: int
    context: str
    field_of_expertise: str
    web_search: bool
    llm_name: str
    api_key: str
