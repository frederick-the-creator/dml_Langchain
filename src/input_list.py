from typing import List, Dict
from src.file_processor import chunk_text
from src.utils import load_json_data
from langchain_core.utils.function_calling import tool_example_to_messages


def retrieve_reference_examles()


def create_input_list(file_content: str, examples_path: str, lines_per_chunk: int = 10) -> List[Dict[str, any]]:
    """
    Creates the input list for the LangChain runnable by splitting the file content into chunks
    and attaching processed reference examples to each chunk.

    Args:
        file_content (str): The full text content from the file.
        examples_path (str): Path to the JSON file containing reference examples.
        lines_per_chunk (int, optional): Number of lines per text chunk. Defaults to 10.

    Returns:
        List[Dict[str, any]]: A list of dictionaries where each dictionary has:
            - "text": A chunk of the text.
            - "examples": The processed reference examples.
    """
    chunks = chunk_text(file_content, lines_per_chunk=lines_per_chunk)
    raw_examples = load_json_data(examples_path)
    processed_examples = tool_example_to_messages(raw_examples)
    input_list = [{"text": chunk, "examples": processed_examples} for chunk in chunks]
    return input_list
