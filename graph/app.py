
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from langgraph.graph import END, StateGraph
from typing import List, TypedDict
from graph.state import GraphState
from graph.conditional_edges import decide_to_generate
from graph.nodes import transform_query, retrieve, grade_documents, websearch, generate

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("transform_query", transform_query) 
workflow.add_node("retrieve", retrieve)  # retrieve documents
workflow.add_node("grade_documents", grade_documents)  # grade documents
workflow.add_node("websearch", websearch)  # websearch
workflow.add_node("generate", generate)  # generate code

workflow.set_entry_point("transform_query")

workflow.add_edge("transform_query", "retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges("grade_documents", decide_to_generate, {
    "websearch": "websearch", 
    "generate": "generate"})
    
workflow.add_edge("websearch", "grade_documents")

workflow.add_edge("generate", END)

app = workflow.compile()



if __name__ == "__main__":
    question = "Create Streamlit application with title AI-Ghostwriter and description AI-enabled writing tool. It should have a sidebar with a selectbox widget that allows users to select a language model and input text for Api Keys.  The main area should display select type of text generation (e.g. poetry, code, etc.), once user selects the type of text, the main area shuld display text input and a button to generate text. The generated text should be displayed below the input"
    
    url = "https://docs.streamlit.io/"
    
    max_depth = 5
    
    context = load_docs(url, max_depth)
    
    expertise_field = "Streamlit application development"

    solution = app.invoke({"messages": [("user", question)], "iterations": 0, "context": context, "expertise_field": expertise_field})

    print(solution["generation"])