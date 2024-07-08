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
                    You are an expert in improving input questions related to a specific field for vector store search optimization.
                    """
                ),
                (
                    "human",
                    """
                    Field of expertise: {field_of_expertise}
                    Original question: {question}
                    
                    Improve the question to ensure it is clear, concise, and semantically rich.
                    
                    Improved question:
                    """
                )
            ]
        )
        self.chain = self.re_write_prompt | self.llm | StrOutputParser()
    
    def invoke(self, input_data):
        return self.chain.invoke(input_data)