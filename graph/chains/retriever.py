from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from graph.utils import load_embeddings

def get_retriever(api_key, llm_name):

    embedding = load_embeddings(api_key=api_key, llm_name=llm_name)
    try:
        chroma_dir = ".chroma/"
        retriever = Chroma(collection_name="local-rag", persist_directory=chroma_dir, embedding_function=embedding).as_retriever()
        return retriever
    except Exception as e:
        raise Exception(f"Unable to get retriever: {e}")