from langchain_core.pydantic_v1 import BaseModel, Field

    
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents"""
    binary_score: str = Field(description="Documents are relevant to the question, 'yes' or 'no'")
    
class QuestionRewriter(BaseModel):
    """Rewritten question"""
    improved_question: str = Field(description="Rewritten improved question")
    reasoning: str = Field(description="Reasoning behind the question rewrite")
