from langchain_core.pydantic_v1 import BaseModel, Field

class Code(BaseModel):
    """Code output"""
    prefix: str = Field(description="Description of the problem and approach")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements")
    description = "Schema for code solutions to questions about Streamit application development."
    
    

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents"""
    binary_score: str = Field(
        ..., description="Documents are relevant to the question, 'yes' or 'no'")
        

class GradeAnswer(BaseModel):
    """Binary score to assess answer addresses question."""
    binary_score: str = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )
    reasoning: str = Field(description = "Reasoning about the binary score given")
    
class ReflectReasoning:
    reflections: str = Field(description="A detailed analysis of why the initial answer was not useful and specific aspects that need improvement.")
    improved_question: str = Field(description="A newly formulated question based on the reflections, designed to better address the user's original query.")

