from typing import Any, Dict
from graph.entities import GraphState
from graph.chains.retriever import get_retriever


def retrieve(state: GraphState) -> Dict[str, Any]:
    """
    Retrieve documents based on the state of the graph.
    
    Args:
        state: The current state of the graph.
        
    Returns:
        A dictionary containing the retrieved documents.
    """
    
    print("<---RETRIEVE---")
    
    question = state["improved_question"]
  
    retriever = get_retriever()

    documents = retriever.invoke(question)
    
    print("----RETRIEVE---->")
    
    return {"context": documents}
    
