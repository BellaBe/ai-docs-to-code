from typing import Any, Dict
from graph.entities import GraphState
from dal.document_database import get_retriever


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
    llm_name = state["llm_name"]
    api_key = state["api_key"]
  
    retriever = get_retriever()

    documents = retriever.invoke(question)
    
    print("----RETRIEVE---->")
    
    return {"context": documents}
    
