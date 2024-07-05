import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from graph.utils import load_LLM
from graph.entities.models import Code


from langchain_core.prompts import ChatPromptTemplate
from graph.utils import load_LLM
from graph.entities.models import Code

class CodeGenerationChain:
    def __init__(self, api_key, llm_name):
        self.llm = load_LLM(api_key, llm_name)
        self.code_gen_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a coding assistant with expertise in {field_of_expertise} \n 
                    Here is a set of documentation:  
                    \n ------- \n  
                    {context} 
                    \n ------- \n 
                    Answer the user question based on the above provided documentation. 
                    Ensure any code you provide can be executed with all required imports and variables defined. 
                    Structure your answer: 
                    1) a prefix describing the code solution, 
                    2) the imports, 
                    3) the functioning code block. \n
                    Invoke the code tool to structure the output correctly.
                    Here is the user question: {question}
                    Answer:
                    """,
                ),
            ]
        )
        self.chain = self.code_gen_prompt | self.llm.with_structured_output(Code)

    def invoke(self, input_data):
        return self.chain.invoke(input_data)
