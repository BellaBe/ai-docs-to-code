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

