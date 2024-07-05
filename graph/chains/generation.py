from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

class Code(BaseModel):
    """Code output"""
    prefix: str = Field(description="Description of the problem and approach")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements")
    description = "Schema for code solutions to questions about Streamit application development."

code_gen_prompt = ChatPromptTemplate.from_messages(
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

llm = ChatGroq(model="llama3-70b-8192")

generation_chain = code_gen_prompt | llm.with_structured_output(Code)


if __name__ == "__main__":
    
    user_query = ""
    docs_url = "https://docs.streamlit.io/"
    retriever = get_retriever(docs_url=docs_url, max_depth=5)
    docs = retriever.invoke( "How to create 2 tabs element one named books and the other one authors.")

    docs_string = ""
    
    for doc in docs:
        docs_string += doc.page_content + "\n"
        
    res = generation_chain.invoke({"context": docs_string, "question": user_query, "expertise_field": "Streamlit"})
    
    print("RESULT====", res)



