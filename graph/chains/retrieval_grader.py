from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from graph.utils import load_LLM
from graph.entities.models import GradeDocuments


class RetrievalGraderChain:
    def __init__(self, api_key, llm_name):
        self.llm = load_LLM(api_key, llm_name)
        self.grade_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a grader assessing the relevance of a retrieved document to a user question.
                    """
                ),
                (
                    "human",
                    """
                    Retrieved document: {document}
                    User question: {question}
                    
                    If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. 
                    Provide a binary score 'yes' or 'no' to indicate whether the document is relevant to the question.
                    
                    Relevance score:
                    """
                )
            ]
        )
        self.chain = self.grade_prompt | self.llm.with_structured_output(GradeDocuments)
    
    def invoke(self, input_data):
        return self.chain.invoke(input_data)