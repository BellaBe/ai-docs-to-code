from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.schema.output_parser import StrOutputParser

from graph.utils import load_LLM


class CodeGenerationChain:
    def __init__(self, api_key, llm_name):
        self.llm = load_LLM(api_key, llm_name)
        self.code_gen_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a coding assistant with expertise in {field_of_expertise}. You will be provided with a set of 
                    latest documentation relative to {field_of_expertise} and user's question. Your task is to generate a 
                    code solution to answer the user's question based on the provided latest documentation and your personal 
                    knowledge. Latest  documentation should prevail over your personal knowledge.
                    Ensure your solution is comprehensive and addresses the user's question in detail. Ensure any code you 
                    provided in the solution can be executed with all required imports and variables defined. Ensure the code 
                    is functional and complete. Your response should contain explanation and code block, nothing else. Ensure to surround code black with backticks.
                    """
                ),
                (
                    "human",
                    """
                    Documentation: {context}
                    User question: {question}
                    
                    Code solution:
                    """
                )
            ]
        )
        self.chain = self.code_gen_prompt | self.llm | StrOutputParser()

    def invoke(self, input_data):
        return self.chain.invoke(input_data)
