from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.pydantic_v1 import BaseModel, Field

from langgraph.graph import END, StateGraph
from typing import List, TypedDict
from graph.entities import GraphState
from graph.edges import decide_to_evaluate_code, decide_to_finish
from graph.nodes import transform_question, retrieve_knowledge, grade_knowledge, generate_code, grade_code, evaluate_code, reflect
from dal.document_database import ingest_docs


workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("transform_query", transform_question) 
workflow.add_node("retrieve_knowledge", retrieve_knowledge)  # retrieve documents
workflow.add_node("grade_knowledge", grade_knowledge)  # grade documents
workflow.add_node("generate_code", generate_code)  # generate code
workflow.add_node("grade_code", grade_code)
workflow.add_node("evaluate_code", evaluate_code)
workflow.add_node("reflect", reflect)

workflow.set_entry_point("transform_query")
workflow.add_edge("transform_query", "retrieve_knowledge")
workflow.add_edge("retrieve_knowledge", "grade_knowledge")
workflow.add_edge("grade_knowledge", "generate_code")
workflow.add_edge("generate_code", "grade_code")

workflow.add_conditional_edges("grade_code", decide_to_evaluate_code, {
    "evaluate_code": "evaluate_code",
    "reflect": "reflect"
})

workflow.add_edge("reflect", "retrieve_knowledge")

workflow.add_conditional_edges("evaluate_code", decide_to_finish, {
    "end": END,
    "reflect": "reflect"
})


flow = workflow.compile()

#flow.get_graph().draw_mermaid_png(output_file_path="graph.png")
