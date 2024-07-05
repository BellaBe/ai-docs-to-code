import os
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
                    As an expert in {field_of_expertise}, your task is to assess the relevance of a retrieved document to a user question. Carefully analyze whether the document contains keywords or semantic meanings closely related to the user question. Consider the context, specificity, and direct relation to the question. Provide a binary score of 'yes' or 'no' to indicate whether the document is relevant to the question.

                    Retrieved document: {document}

                    User question: {question}

                    Relevance score:
                    """
                )

            ]
        )
        self.chain = self.grade_prompt | self.llm.with_structured_output(GradeDocuments)
    
    def invoke(self, input_data):
        return self.chain.invoke(input_data)