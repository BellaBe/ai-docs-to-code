import streamlit as st
from langchain_openai import OpenAI
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings


MODEL_MAP = {
    "OpenAI GPT-3.5 Turbo": {
        "class": OpenAI,
        "params": {
            "temperature": 0,
            "api_key": None  # To be set dynamically
        },
        "embedding_class": OpenAIEmbeddings,
        "embedding_params": {
            "api_key": None  # To be set dynamically
        }
    },
    "Groq LLaMA3 70b": {
        "class": ChatGroq,
        "params": {
            "model_name": "llama3-70b-8192",
            "groq_api_key": None  # To be set dynamically
        },
        "embedding_class": HuggingFaceEmbeddings,
        "embedding_params": {
            "model_name": "sentence-transformers/all-MiniLM-L6-v2"  # Example model
        }
    },
    "Groq Mixtral 8x7b": {
        "class": ChatGroq,
        "params": {
            "model_name": "mixtral-8x7b-32768",
            "groq_api_key": None  # To be set dynamically
        },
        "embedding_class": HuggingFaceEmbeddings,
        "embedding_params": {
            "model_name": "sentence-transformers/all-MiniLM-L6-v2"  # Example model
        }
    }
}