from bs4 import BeautifulSoup as Soup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_chroma import Chroma
from chromadb import PersistentClient

def ingest_docs(docs_url, max_depth):
    try:

        loader = RecursiveUrlLoader(
            url=docs_url,
            prevent_outside=True,
            max_depth=max_depth,
            extractor=lambda x: Soup(x, "html.parser").text
        )
        docs = loader.load()
        for doc in docs:
            if doc.metadata.get("language") is None:
                doc.metadata["language"] = "English"
        
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250, chunk_overlap=0)
        doc_splits = text_splitter.split_documents(docs)
        
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        
        Chroma.from_documents(documents=doc_splits, embedding=embedding_function, collection_name="local-rag", persist_directory=".chroma")
        
        return 

    except Exception as e:
        raise Exception(f"Unable to ingest docs: {e}")
        
        
def get_retriever():
    try:
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        chroma_client = PersistentClient(path=".chroma/")
        
        collection = chroma_client.get_or_create_collection(name="local-rag")
        
        chroma_instance = Chroma(
            collection_name="local-rag",
            embedding_function=embedding_function,
            persist_directory=".chroma/",
            client=chroma_client
        )
        
        retriever = chroma_instance.as_retriever()
        return retriever
    except Exception as e:
        raise Exception(f"Unable to get retriever: {e}")
        
def delete_collection():
    try:
        collection_name = "local-rag"
        chroma_client = PersistentClient(path=".chroma")
        chroma_client.delete_collection(collection_name)
        print(f"Collection {collection_name} deleted successfully.")
    except Exception as e:
        raise Exception(f"Unable to delete collection: {e}")
        
def check_collection_exists():
    try:
        persist_directory = ".chroma"
        chroma_client = PersistentClient(path=persist_directory)
        try:
            chroma_client.get_collection(name="local-rag")
            return True
        except ValueError:
            return False
    except Exception as e:
        raise Exception(f"Unable to check collection existence: {e}")