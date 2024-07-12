# main.py
import streamlit as st
import os
import time
import json
import re
from typing import Tuple
from graph.entities import GraphState
from graph.app import flow
from dotenv import load_dotenv
from dal.document_database import delete_collection, check_collection_exists, ingest_docs

load_dotenv()

DATA_FILE = "session.json"


def set_header():
    st.set_page_config(
        page_title="Code Generation from Docs",
        page_icon=":page_with_curl:",
        layout="wide"
    )
    st.title("Code Generation from Docs :page_with_curl:")
    st.write("This app generates code solutions based on the user question and documentation of the library")


def extract_components(text: str) -> Tuple[str, str, str]:
    pattern = re.compile(r"(.*?)(```[\s\S]*?```)(.*)", re.DOTALL)
    match = pattern.search(text)
    if match:
        initial_text = match.group(1).strip()
        code_block = match.group(2).strip()
        final_text = match.group(3).strip()
        return initial_text, code_block, final_text
    else:
        return "", text.strip(), ""


def save_data_to_file(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)


def load_data_from_file():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return None


def delete_data_file():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)


def handle_ingest_docs():
    with st.spinner("Ingesting docs..."):
        try:
            ingest_docs(docs_url=st.session_state.docs_url_input,
                        max_depth=st.session_state.max_depth_input)
            st.session_state.docs_ingested = True
            st.session_state.ingested_docs_values = (
                st.session_state.field_of_expertise_input, st.session_state.docs_url_input, st.session_state.max_depth_input)
            save_data_to_file({
                "field_of_expertise": st.session_state.field_of_expertise_input,
                "docs_url": st.session_state.docs_url_input,
                "max_depth": st.session_state.max_depth_input
            })
        except Exception as e:
            st.error(f"Failed to ingest docs: {e}")


def handle_submit_model():
    st.session_state.model_set = True
    st.session_state.loaded_model_values = (
        st.session_state.llm_name, st.session_state.api_key)


def handle_delete_collection():
    with st.spinner("Deleting collection..."):
        try:
            delete_collection()
            delete_data_file()
            st.session_state.docs_ingested = False
            st.session_state.field_of_expertise = ""
            st.session_state.docs_url = ""
            st.session_state.max_depth = 10
            st.session_state.ingested_docs_values = None
            st.success("Collection deleted successfully.")
        except Exception as e:
            st.error(f"Failed to delete collection: {e}")

def handle_change_model():
    st.session_state.model_set = False
    st.session_state.loaded_model_values = None

def mask_api_key(api_key):
    if len(api_key) > 6:
        return f"{api_key[:5]}{'*' * (len(api_key) - 35)}{api_key[-4:]}"
    else:
        return api_key

set_header()

# Initialize session state variables
if "model_set" not in st.session_state:
    st.session_state.model_set = False

if "llm_name" not in st.session_state:
    # Set default value that exists in the selectbox options
    st.session_state.llm_name = "OpenAI GPT-3.5 Turbo"

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "docs_ingested" not in st.session_state:
    st.session_state.docs_ingested = check_collection_exists()

if "field_of_expertise" not in st.session_state:
    st.session_state.field_of_expertise = ""

if "docs_url" not in st.session_state:
    st.session_state.docs_url = ""

if "max_depth" not in st.session_state:
    st.session_state.max_depth = 10

if "ingested_docs_values" not in st.session_state:
    st.session_state.ingested_docs_values = None

if "loaded_model_values" not in st.session_state:
    st.session_state.loaded_model_values = None

# Load data from file if collection exists and data is not already set
if st.session_state.docs_ingested and st.session_state.ingested_docs_values is None:
    data = load_data_from_file()
    if data:
        st.session_state.ingested_docs_values = (
            data["field_of_expertise"], data["docs_url"], data["max_depth"]
        )
        st.session_state.field_of_expertise = data["field_of_expertise"]
        st.session_state.docs_url = data["docs_url"]
        st.session_state.max_depth = data["max_depth"]

# Model form (only one form for setting the model and API key)
if not st.session_state.model_set:
    with st.form(key='model_form'):
        col1, col2, col3 = st.columns(
            3, gap="medium", vertical_alignment="bottom")
        with col1:
            st.selectbox("Select LLM provider and model type", [
                         "OpenAI GPT-3.5 Turbo", "Groq LLaMA3 70b", "Groq Mixtral 8x7b"], key="llm_name")
        with col2:
            st.text_input("API Key", type="password",
                          placeholder="Ex: sk-2t... or gsk_mc12...", key="api_key")
        with col3:
            st.form_submit_button('Set model', on_click=handle_submit_model)

# Display model details and allow changing the model
else:
    with st.expander("Model details"):
        st.text(f"Model name: {st.session_state.loaded_model_values[0]}")
        st.text(
            f"API key: {mask_api_key(st.session_state.loaded_model_values[1])}")
        if st.button("Change Model", on_click=handle_change_model):
            st.success("Model settings cleared. Please set the model again.")

# Document ingestion form
if not st.session_state.docs_ingested:
    with st.form(key='docs_form'):
        col1, col2, col3, col4 = st.columns(
            4, gap="medium", vertical_alignment="bottom")
        with col1:
            st.text_input("Field of expertise", placeholder="Ex: Streamlit, Langchain, etc.",
                          key="field_of_expertise_input", value=st.session_state.field_of_expertise)
        with col2:
            st.text_input("Documentation URL", placeholder="Ex: https://docs.streamlit.io/",
                          key="docs_url_input", value=st.session_state.docs_url)
        with col3:
            st.number_input("Max depth for web search", min_value=1,
                            value=st.session_state.max_depth, key="max_depth_input")
        with col4:
            st.form_submit_button('Ingest docs', on_click=handle_ingest_docs)
else:
    with st.expander("Ingested docs details"):
        st.text(
            f"Field of expertise: {st.session_state.ingested_docs_values[0]}")
        st.text(f"Docs URL: {st.session_state.ingested_docs_values[1]}")
        st.text(f"Max depth: {st.session_state.ingested_docs_values[2]}")
        if st.button("Delete Collection", on_click=handle_delete_collection):
            st.success("Collection deleted successfully.")

with st.container():
    with st.form(key='question_form', clear_on_submit=True):
        user_question = st.text_area(
            "Enter your question here", placeholder="Ex: How to create a sidebar", disabled=not st.session_state.docs_ingested)
        if st.form_submit_button("Generate code", disabled=not st.session_state.docs_ingested or not st.session_state.model_set):
            state = GraphState(
                question=user_question,
                improved_question=None,
                reasoning_for_improved_question=None,
                field_of_expertise=st.session_state.ingested_docs_values[0],
                context=[],
                solution=None,
                errors=[],
                iterations=1,
                llm_name=st.session_state.loaded_model_values[0],
                api_key=st.session_state.loaded_model_values[1],
            )

            try:
                with st.spinner("Generating code..."):
                    result = flow.invoke(state)
                    st.write(f"Original question: {result['question']}")
                    st.write(
                        f"LLM improved question: {result['improved_question']}")
                    solution = result.get("solution")
                    errors = result["errors"]
                    iterations = result["iterations"]
                    static_analysis_results = result["static_analysis_results"]
                    st.error(
                        f"During code evaluation, the following errors occured: {errors}")
                    st.warning(
                        f"Here are static analysis results: {static_analysis_results}")
                    st.info(f"Number of performed iterations: {iterations}")

                    initial_text, code_block, final_text = extract_components(
                        solution)

                    if initial_text != "":
                        st.success(initial_text)

                    st.code(code_block, language="python")

                    if final_text != "":
                        st.success(final_text)

            except Exception as e:
                st.error(f"Failed to generate code. Error: {e}")
