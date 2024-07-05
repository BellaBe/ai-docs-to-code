from typing import Any, Dict

from graph.entities import GraphState
from graph.chains.retrieval_grader import RetrievalGraderChain

def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the user question. If any document is not relevant, we will set a flag to run web search.
    
    Args:
        state(dict): The current state of the graph.
    
    Returns:
        state(dict): Filtered our irrelevant documents and updated web_search flag.
    """
    
    print("---GRADE DOCUMENTS---")
    
    question = state["improved_question"]
    documents = state["context"]
    field_of_expertise = state["field_of_expertise"]
    api_key = state["api_key"]
    llm_name = state["llm_name"]
    
    filtered_docs = []
    web_search = False
    
    retrieval_grader = RetrievalGraderChain(api_key, llm_name)
    
    for d in documents:
        score = retrieval_grader.invoke({
            "question": question,
            "document": d.page_content,
            "field_of_expertise": field_of_expertise
        })
        
        grade = score.binary_score
        if grade == "yes":
            print("---DOCUMENT IS RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---DOCUMENT IS NOT RELEVANT---")
            print("NON-RELEVANT DOCUMENT: ", d.page_content)
            web_search = True
            continue
    
    
    return {"context": filtered_docs, "web_search": web_search}