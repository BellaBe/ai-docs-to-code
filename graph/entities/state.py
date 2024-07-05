from typing import TypedDict, List

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: User question
        improved_question: Improved user question by the system
        error : Binary flag for control flow to indicate whether test error was tripped
        messages : With user question, error messages, reasoning
        generation : Code solution
        iterations : Number of tries
        context: Documentation of the library
        field_of_expertise: Field of assistant expertise 
        web_search: Flag for web search
    """
    
    question: str
    improved_question: str
    generation: str
    context: str
    field_of_expertise: str
    web_search: bool
    interations: int
 