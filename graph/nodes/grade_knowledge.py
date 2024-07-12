from typing import Any, Dict
from graph.entities import GraphState
from graph.chains.knowledge_grader import KnowledgeGraderChain

def grade_knowledge(state: GraphState) -> GraphState:
    """
    Determines whether the retrieved documents are relevant to the user question. 
    If any document is not relevant, it will be filtered out.

    Args:
        state (GraphState): The current state of the graph.

    Returns:
        state (GraphState): Updated state with filtered documents.
    """
    
    print("<----GRADING EXTRACTED KNOWLEDGE----")
    
    # Extract necessary information from the state
    question = state["improved_question"]
    documents = state["context"]
    field_of_expertise = state["field_of_expertise"]
    api_key = state["api_key"]
    llm_name = state["llm_name"]
    
    # Initialize the KnowledgeGraderChain
    knowledge_grader = KnowledgeGraderChain(api_key, llm_name)
    
    # Filter documents based on their relevance
    filtered_docs = [
        d for d in documents 
        if knowledge_grader.invoke({
            "question": question,
            "document": d.page_content,
            "field_of_expertise": field_of_expertise
        }).binary_score == "yes"
    ]
    
    # Update the state with the filtered documents
    state["context"] = filtered_docs
    
    print("----GRADING EXTRACTED KNOWLEDGE---->")
    
    return state
