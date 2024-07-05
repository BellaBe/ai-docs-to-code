__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import os
import time
import shutil
from graph.graph import app
from graph.ingestion import ingest_docs
from graph.utils import load_LLM
from graph.entities import GraphState

base_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    layout="wide",
    page_title="Code Generator from Documentation"
)

# Title with icon
st.title("Code Generation from Docs")
st.write("This app generates code solutions based on the user question and documentation of the library.")

st.sidebar.title("Settings")

@st.cache_resource
def initialize_app(api_key, llm_name):
    return load_LLM(api_key, llm_name)

if "llm_name" not in st.session_state:
    st.session_state.llm_name = None

if "api_key" not in st.session_state:
    st.session_state.api_key = None

if "llm" not in st.session_state:
    st.session_state.llm = None

if "docs_ingested" not in st.session_state:
    st.session_state.docs_ingested = False
    
if "spinner_disabled" not in st.session_state:
    st.session_state.spinner_disabled = False

llm_name_input = st.sidebar.selectbox(
    "Select LLM provider and model type",
    ["OpenAI GPT-3.5 Turbo", "Groq LLaMA3 70b", "Groq Mixtral 8x7b"],
    key="llm_name_input"
)

api_key_input = st.sidebar.text_input(
    "API Key", type="password", placeholder="Ex: sk-2t... or gsk_mc12...", key="api_key_input"
)

# Update session state with inputs
if api_key_input:
    st.session_state.api_key = api_key_input

if llm_name_input:
    st.session_state.llm_name = llm_name_input

def handle_ingest():
    docs_url = st.session_state.docs_url
    max_depth = st.session_state.max_depth
    llm_name = st.session_state.llm_name
    api_key = st.session_state.api_key
    with st.spinner("Ingesting docs..."):
        context = ingest_docs(docs_url=docs_url, max_depth=int(max_depth), base_dir=base_dir, llm_name=llm_name, api_key=api_key)
    st.session_state.docs_ingested_values = (st.session_state.field_of_expertise, st.session_state.docs_url, st.session_state.max_depth, context)
    st.session_state.docs_ingested = True

def flush_docs():
    chroma_dir = os.path.join(base_dir, ".chroma/")
    if os.path.exists(chroma_dir):
        shutil.rmtree(chroma_dir)
    st.session_state.docs_ingested = False
    st.session_state.docs_ingested_values = None

if st.button("Initialize App"):
    if st.session_state.api_key and st.session_state.llm_name:
        st.session_state.llm = initialize_app(st.session_state.api_key, st.session_state.llm_name)
        if st.session_state.llm:
            st.success("App initialized successfully with the selected LLM and API Key.")
        else:
            st.error("Failed to initialize the app. Please check your API key and LLM name.")
    else:
        st.error("Please provide both the API key and select the LLM provider.")

if st.session_state.llm:
    if not st.session_state.docs_ingested:
        with st.form(key='docs_form'):
            col1, col2, col3 = st.columns(3, gap="medium")
            with col1:
                field_of_expertise = st.text_input("Field of expertise", placeholder="Ex: Streamlit, Langchain, etc.", key="field_of_expertise")
            with col2:
                docs_url = st.text_input("Documentation URL", placeholder="Ex: https://docs.streamlit.io/", key="docs_url")
            with col3:
                max_depth = st.number_input("Max depth for web search", value=5, key="max_depth")
            
            submit = st.form_submit_button('Ingest docs', on_click=handle_ingest)
    else:
        with st.container():
            st.write(f'Field of expertise: {st.session_state.docs_ingested_values[0]}, docs: {st.session_state.docs_ingested_values[1]}, max depth: {st.session_state.docs_ingested_values[2]}.')
            st.button('Flush docs from memory', type="secondary", on_click=flush_docs)

    with st.container():
        user_question = st.text_area("Enter your question here", placeholder="Ex: How to create a sidebar", key="user_question", disabled=not st.session_state.docs_ingested)
        
        print("USER QUESTION: ", user_question)

        btn = st.button("Generate code", disabled=not st.session_state.docs_ingested, key="generate_code_btn")

        if btn:
            context = st.session_state.docs_ingested_values[3]
            expertise_field = st.session_state.docs_ingested_values[0]
            state = GraphState(
                context=context,
                question=user_question,
                field_of_expertise=expertise_field,
                improved_question="",
                llm_name=st.session_state.llm_name,
                api_key=st.session_state.api_key,
                error=False,
                messages="",
                generation="",
                iterations=0,
                web_search=False
            )
            
            solution = app.invoke(state)

            with st.spinner("Generating code..."):
                time.sleep(5)
            st.write(solution["generation"].prefix)
            imports = solution["generation"].imports
            code = solution["generation"].code
            st.code(code, language="python")
else:
    st.warning("Please initialize the app with the selected LLM and API Key.")
