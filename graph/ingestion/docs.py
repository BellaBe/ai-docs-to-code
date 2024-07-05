from bs4 import BeautifulSoup as Soup
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import RecursiveUrlLoader

    
def ingest_docs(docs_url, max_depth, base_dir):
    try:
        chroma_dir = os.path.join(base_dir, ".chroma/")
        loader = RecursiveUrlLoader(url=docs_url, max_depth=max_depth, extractor=lambda x: Soup(x, "html.parser").text)

        docs = loader.load()
        
        for doc in docs:
            if doc.metadata.get("language") is None:
                doc.metadata["language"] = "English"
        
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250, chunk_overlap=0)
        
        doc_splits = text_splitter.split_documents(docs)
        
        Chroma.from_documents(documents=doc_splits, embedding=OpenAIEmbeddings(), collection_name="local-rag", persist_directory=chroma_dir)
        
        return
    
    except Exception as e:
        raise Exception(f"Unable to ingest docs: {e}")
    
