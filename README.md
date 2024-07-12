# Docs-to-Code RAG Application

Welcome to the Docs-to-Code RAG application repository! This project demonstrates how to build a Reasoning and Answer Generation (RAG) system using LangChain, LangGraph, and Streamlit. The application ingests documentation, allows users to query it, and generates code solutions based on the provided documentation.

## Project Overview

This application consists of several key components:
- **Data Ingestion**: Ingests documentation and stores it in a vector store.
- **Query Transformation**: Transforms user queries to optimize for similarity search.
- **Knowledge Retrieval**: Performs semantic search to retrieve relevant documentation.
- **Knowledge Grading**: Grades the retrieved knowledge for relevance.
- **Code Generation**: Generates code based on the refined query and relevant documentation.
- **Code Evaluation**: Evaluates the generated code for correctness.
- **Code Fixing**: Fixes any errors in the generated code.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.8+
- Virtualenv (optional but recommended)

### Installation

1. **Clone the repository**
    ```sh
    git clone https://github.com/BellaBe/ai-docs-to-code
    cd docs-to-code-rag
    ```

2. **Create and activate a virtual environment**
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install the required dependencies**
    ```sh
    pip install -r requirements.txt
    ```

### Starting the Application

To start the application, run the following command:

```sh
streamlit run main.py
```
