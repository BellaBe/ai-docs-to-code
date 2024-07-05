import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from graph.utils import load_LLM

    
class QuestionRewriterChain:
    def __init__(self, api_key, llm_name):
        self.llm = load_LLM(api_key, llm_name)
        self.re_write_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", 
                    """
                        As an expert in {field_of_expertise}, your task is to improve input questions related to {field_of_expertise} topic for vector store search optimization. Analyze the input to understand the underlying semantic intent and meaning. Ensure the improved question is related to {field_of_expertise} topic, ensure the improved question is clear, concise, and semantically rich. Return only the improved question. Note: Do not provide any additional context or information.

                        Original question: {question}

                        Improved question:
                    """
                    )
            ]
        )
        self.chain = self.re_write_prompt | self.llm | StrOutputParser()
    
    def invoke(self, input_data):
        return self.chain.invoke(input_data)