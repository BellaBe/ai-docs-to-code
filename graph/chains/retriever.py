from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings



def get_retriever():
    try:
        chroma_dir = ".chroma/"
        retriever = Chroma(collection_name="local-rag", persist_directory=chroma_dir, embedding_function=OpenAIEmbeddings()).as_retriever()
        return retriever
    except Exception as e:
        
        raise Exception(f"Unable to get retriever: {e}")