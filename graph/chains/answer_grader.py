import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from graph.utils import load_LLM
from graph.entities.models import GradeAnswer


class AnswerGraderChain:
    def __init__(self, api_key, llm_name):
        self.llm = load_LLM(api_key, llm_name)
        self.grade_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a grader expert in assessing whether an answer provided by an LLM addresses/resolves a question.
                    """
                ),
                (
                    "human",
                    """
                    User question: {question}
                    LLM answer: {generation}
                    
                    The LLM answer should be structured as follows:
                    1) a prefix describing the code solution, 
                    2) the imports, 
                    3) the functioning code block.
                    
                    Check and comment on the completeness of each part:
                    - Prefix: Describe the code solution.
                    - Imports: Ensure all necessary imports are included.
                    - Code: Ensure the code block is functional and complete.

                    If any part is missing or incomplete, include this in your assessment.
                    
                    Give a binary score 'yes' or 'no'. 'Yes' means that the answer resolves the question and provide the reason behind your decision.
                    
                    Invoke The GradeAnswer tool to generate your output.
                    """
                )
            ]
        )
        self.chain = self.grade_prompt | self.llm.with_structured_output(GradeAnswer)
    
    def invoke(self, input_data):
        return self.chain.invoke(input_data)
