import streamlit as st
import time
import os

from graph.app import app
from ui.models import MODEL_MAP
from graph.ingestion import ingest_docs
import asyncio
import shutil

base_dir = os.path.dirname(os.path.abspath(__file__))

def load_LLM(api_key, llm_name):
    model_config = MODEL_MAP[llm_name]
    model_class = model_config["class"]
    params = model_config["params"]

    # Set the appropriate API key parameter
    if "api_key" in params:
        params["api_key"] = api_key
    elif "groq_api_key" in params:
        params["groq_api_key"] = api_key

    llm = model_class(**params)
    return llm


def get_llm_name():
    llm_name = st.sidebar.selectbox(
        "Select LLM provider and model type",
        list(MODEL_MAP.keys()),
        key="llm_name_input"
    )
    return llm_name


def get_provider_api_key():
    api_key = st.sidebar.text_input(
        "API Key", type="password", placeholder="Ex: sk-2t... or gsk_mc12...", key="api_key_input")
    return api_key


def is_api_key_valid(api_key):
    return api_key is not None and (api_key.startswith("sk-") or api_key.startswith("gsk_"))


def load_embeddings(api_key, llm_name):
    model_config = MODEL_MAP[llm_name]
    embedding_class = model_config["embedding_class"]
    embedding_params = model_config["embedding_params"]

    # Set the appropriate API key parameter
    if "api_key" in embedding_params:
        embedding_params["api_key"] = api_key

    embeddings = embedding_class(**embedding_params)
    return embeddings


def handle_ingest():
    docs_url = st.session_state.docs_url
    max_depth = st.session_state.max_depth
    with st.spinner("Ingesting docs..."):
        ingest_docs(docs_url=docs_url, max_depth=int(max_depth), base_dir=base_dir)
    st.session_state.docs_ingested_values = (st.session_state.field_of_expertise, st.session_state.docs_url, st.session_state.max_depth)
    st.session_state.docs_ingested = True
  
def show_docs_ingested_values():
    st.session_state.docs_ingested_values = (st.session_state.field_of_expertise, st.session_state.docs_url, st.session_state.max_depth)
    st.session_state.docs_ingested = True

def flush_docs():
    chroma_dir = os.path.join(base_dir, ".chroma/")
    if os.path.exists(chroma_dir):
        shutil.rmtree(chroma_dir)
    st.session_state.docs_ingested = False
    st.session_state.docs_ingested_values = None
    

st.set_page_config(
    layout="wide", 
    page_title="Code generator from documentation"
)

# Title with icon
st.title("Code generation from docs")
st.write("This app generates code solutions based on the user question and documentation of the library.")

st.sidebar.title("Settings")


if "llm_name" not in st.session_state:
    st.session_state.llm_name = None

if "api_key" not in st.session_state:
    st.session_state.api_key = None
    
if "docs_ingested" not in st.session_state:
    st.session_state.docs_ingested = False
    
if "spinner_disabled" not in st.session_state:
    st.session_state.spinner_disabled = False
    
    
st.session_state.llm_name = get_llm_name()
st.session_state.api_key = get_provider_api_key()

if not st.session_state.llm_name or not st.session_state.api_key:
    st.success("👈 Please select the LLM provider/model type and insert associated API Key.")


 
if not st.session_state.docs_ingested:
    with st.form(key='docs_form'):
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            field_of_expertise = st.text_input("Field of expertise", placeholder="Ex: Streamlit, Langchain, etc.", key="field_of_expertise")
        with col2:
            docs_url = st.text_input("Documentation URL", placeholder="Ex: https://docs.streamlit.io/", key="docs_url")
            
        with col3:
            max_depth = st.number_input("Max depth for web search", value=5, key="max_depth")
        
        submit = st.form_submit_button('Ingest docs', on_click=handle_ingest) # Callback changes it to result mode
            
else:
    with st.container(border=True):
        st.write(f'Field of expertise: {st.session_state.docs_ingested_values[0]}, docs: {st.session_state.docs_ingested_values[1]}, max depth: {st.session_state.docs_ingested_values[2]}.')
        st.button('Flush docs from memory', type="secondary", on_click=flush_docs)
    

with st.container(border=True):
    user_question = st.text_area("Enter your question here", placeholder="Ex: How to create a sidebar", key="user_question", disabled=not st.session_state.docs_ingested)

    btn = st.button("Generate code", disabled=not st.session_state.docs_ingested, key="generate_code_btn")

    if btn:
        solution = app.invoke({
            "question": user_question,
            "field_of_expertise": st.session_state.docs_ingested_values[0],
        })
        
        with st.spinner("Generating code..."):
            time.sleep(5)
        st.write(solution["generation"])
        st.write(solution["generation"].prefix)
        imports = solution["generation"].imports
        code = solution["generation"].code
        st.code(code, language="python")


