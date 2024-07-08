import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from graph.utils import load_LLM
from graph.entities.models import ReflectReasoning

class ReflectorChain:
    def __init__(self, api_key, llm_name):
        self.llm = load_LLM(api_key, llm_name)
        self.reflect_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are an expert in reflecting on the current state of the answer generation process and providing insights on how to improve the generated answer.
                    """
                ),
                (
                    "human",
                    """
                    User question: {question}
                    Improved question: {improved_question}
                    Generated answer: {generation}
                    Answer usefulness (yes/no): {is_answer_useful}
                    Reasoning for usefulness assessment: {answer_reasoning}
                    
                    Reflect on the following points:
                    1. Why was the generated answer not useful?
                    2. What specific aspects of the answer need improvement?
                    3. Provide suggestions on how to refine the improved question or approach to better address the user question.
                    
                    Based on your reflections, generate an improved question that incorporates the necessary improvements for better addressing the user question.
                    
                    Your reflections and improved question:
                    """
                )
            ]
        )
        self.chain = self.reflect_prompt | self.llm.with_structured_output(ReflectReasoning)
    
    def invoke(self, input_data):
        return self.chain.invoke(input_data)