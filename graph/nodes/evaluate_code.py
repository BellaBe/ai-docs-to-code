import ast
import re
from typing import List, Tuple

def static_analysis(code: str) -> List[str]:
    """
    Perform static analysis on the provided code.
    
    Args:
        code (str): The code to analyze.
    
    Returns:
        List[str]: A list of error messages, if any.
    """
    errors = []

    # Check for syntax errors
    try:
        ast.parse(code)
    except SyntaxError as e:
        errors.append(f"Syntax error in code: {e}")

    return errors

def extract_text_and_code_blocks(text: str) -> List[Tuple[str, str, str]]:
    """
    Extract text before and after code blocks enclosed in triple backticks, and the code blocks themselves.
    
    Args:
        text (str): The text containing code blocks.
    
    Returns:
        List[Tuple[str, str, str]]: A list of tuples, each containing the prefix, code block with backticks, and suffix.
    """
    pattern = re.compile(r"(.*?)(```.*?```)(.*)", re.DOTALL)
    matches = pattern.findall(text)
    
    results = []
    for match in matches:
        prefix, code_block_with_backticks, suffix = match
        results.append((prefix.strip(), code_block_with_backticks.strip(), suffix.strip()))
    
    return results

def evaluate_code(state: dict) -> dict:
    """
    Evaluate the code in the current state by performing static analysis.
    
    Args:
        state (dict): The current state.
    
    Returns:
        dict: Updated state after evaluation.
    """

    print("<----EVALUATING CODE----")

    # State
    code_solution = state.get("solution")
    
    if code_solution is None or code_solution == "":
        state["errors"].append("Solution is missing")
        print("----EVALUATING CODE: NO SOLUTION----")
        return state

    # Extract text and code blocks
    text_and_code_blocks = extract_text_and_code_blocks(code_solution)
    
    if len(text_and_code_blocks) == 0:
        state["errors"].append("Solution is missing text and code blocks")
        print("----EVALUATING CODE: INVALID SOLUTION----")
        return state

    # Perform static analysis on each code block
    for prefix, code_block_with_backticks, suffix in text_and_code_blocks:
        code_block = re.sub(r'^```.*?\n(.*?)```$', r'\1', code_block_with_backticks, flags=re.DOTALL).strip()
        if not code_block:
            state["errors"].append("Code block is empty")
            print("----EVALUATING CODE: EMPTY CODE BLOCK----")
            return state

        errors = static_analysis(code_block)
        if len(errors) > 0:
            errors = " ".join(errors)
            state["static_analysis_result"] = f"Failed to perform static analysis on code block: {errors}"
            print("----EVALUATING CODE: STATIC ANALYSIS FAILED----")
            return state

    state["static_analysis_results"] = "Success"
    print("----EVALUATING CODE: SUCCESS----")
    return state