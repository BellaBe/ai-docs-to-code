import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)


class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents"""
    binary_score: str = Field(
        ..., description="Documents are relevant to the question, 'yes' or 'no'")


structured_llm_grader = llm.with_structured_output(GradeDocuments)


grade_prompt = ChatPromptTemplate.from_messages(
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

retrieval_grader = grade_prompt | structured_llm_grader
