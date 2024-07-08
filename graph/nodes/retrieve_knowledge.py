from typing import Any, Dict
from graph.entities import GraphState
from dal.document_database import get_retriever

def retrieve_knowledge(state: GraphState) -> Dict[str, Any]:
    """
    Retrieve documents based on the state of the graph.
    
    Args:
        state (GraphState): The current state of the graph.
        
    Returns:
        Dict[str, Any]: New key added to state, context (retrieved documents)
    """
    
    print("<----RETRIEVING KNOWLEDGE----")
    
    question = state["improved_question"]
    retriever = get_retriever()

    documents = retriever.invoke(question)
    
    state["context"] = documents
    
    print("----RETRIEVING KNOWLEDGE---->")
    
    return state
