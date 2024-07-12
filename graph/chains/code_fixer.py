from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.schema.output_parser import StrOutputParser

from graph.utils import load_LLM


class CodeFixerChain:
    def __init__(self, api_key, llm_name):
        self.llm = load_LLM(api_key, llm_name)
        self.code_gen_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a coding assistant with expertise in {field_of_expertise} and exceptional skills in fixing coding errors. 
                    You will be provided with user question, code solution, latest documentation relative to {field_of_expertise} and 
                    errors resulted from previous run. Your task is to fix coding errors. Ensure your solution is comprehensive and 
                    addresses the error. Ensure any code you provide can be executed with all required imports and variables defined. 
                    Ensure the code is functional and complete. Your response should contain explanation and code block, nothing else.
                    Ensure to surround code block with backticks.
                    """
                ),
                (
                    "human",
                    """
                    User question: {question}
                    Solution: {solution}
                    Relevant documentation: {context}
                    Errors: {errors}
                    
                    Solution:
                    """
                )
            ]
        )
        self.chain = self.code_gen_prompt | self.llm | StrOutputParser()

    def invoke(self, input_data):
        return self.chain.invoke(input_data)
