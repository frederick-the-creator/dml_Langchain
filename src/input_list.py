from typing import List, Dict
from src.file_processor import chunk_text
from src.utils import load_json_data
from langchain_core.utils.function_calling import tool_example_to_messages


def retrieve_reference_examles()


def create_input_list(chunks: List[str], examples_path: str) -> List[Dict[str, any]]:
    """
    Creates the input list for the LangChain runnable by attaching processed reference examples
    to each provided text chunk.

    Args:
        chunks (List[str]): A list of text chunks.
        examples_path (str): Path to the JSON file containing reference examples.

    Returns:
        List[Dict[str, any]]: A list of dictionaries where each dictionary has:
            - "text": A text chunk.
            - "examples": The processed reference examples.
    """
    raw_examples = load_json_data(examples_path)
    processed_examples = tool_example_to_messages(raw_examples)
    input_list = [{"text": chunk, "examples": processed_examples} for chunk in chunks]
    return input_list
