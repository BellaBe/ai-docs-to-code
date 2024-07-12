
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from graph.utils import load_LLM
from graph.entities.models import QuestionRewriter

    
class QuestionRewriterChain:
    def __init__(self, api_key, llm_name):
        self.llm = load_LLM(api_key, llm_name)
        self.re_write_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", 
                    """
                    You are an expert in optimizing input questions related to {field_of_expertise} for vector 
                    store similarity search. Your task is to rewrite the user question to improve the search results.
                    """
                ),
                (
                    "human",
                    """
                    User question: {question}
                    
                    Use QuestionRewriter tool to generate your output.
                    
                    QuestionRewriter:
                    """
                )
            ]
        )

        self.chain = self.re_write_prompt | self.llm.with_structured_output(QuestionRewriter)

    def invoke(self, input_data):
        return self.chain.invoke(input_data)    