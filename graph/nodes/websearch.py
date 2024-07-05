from typing import Any, Dict

from langchain.schema import Document
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun

from graph.state import GraphState

web_search_tool = DuckDuckGoSearchRun(max_results=5)

def websearch(state: GraphState) -> Dict[str, Any]:
    print("<----WEB SEARCH----")
    question = state["question"]
    documents = state["context"]
    
    results = web_search_tool.invoke({"query": question})
    
    if type(results) == str:
        joined_result = results
    else:
        joined_result = "\n".join([result["content"] for result in results])
    
    web_results = Document(page_content=joined_result)
    
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
        
    print("----WEB SEARCH---->")
    return {"context": documents, "question": question}
    