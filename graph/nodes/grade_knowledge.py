from typing import Any, Dict
from graph.entities import GraphState
from graph.chains.retrieval_grader import RetrievalGraderChain

def grade_knowledge(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the user question. If any document is not relevant, we will set a flag to run web search.
    
    Args:
        state (GraphState): The current state of the graph.
    
    Returns:
        state (GraphState): Filtered our irrelevant documents and updated web_search flag.
    """
    
    print("<----GRADING EXTRACTED KNOWLEDGE----")
    
    question = state["improved_question"]
    documents = state["context"]
    field_of_expertise = state["field_of_expertise"]
    api_key = state["api_key"]
    llm_name = state["llm_name"]
    
    filtered_docs = []
    
    retrieval_grader = RetrievalGraderChain(api_key, llm_name)
    
    for d in documents:
        score = retrieval_grader.invoke({
            "question": question,
            "document": d.page_content,
            "field_of_expertise": field_of_expertise
        })
        
        grade = score.binary_score
        if grade == "yes":
            filtered_docs.append(d) 
    
    state["context"] = filtered_docs
    
    print("----GRADING EXTRACTED KNOWLEDGE---->")
    return state
