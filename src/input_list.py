from typing import List, Dict
import json
from src.file_processor import chunk_text

def load_reference_examples(examples_path: str) -> List[dict]:
    """
    Loads reference examples from a JSON file located at examples_path.

    Args:
        examples_path (str): Path to the JSON file containing reference examples.

    Returns:
        List[dict]: A list of example dictionaries.
        
    Raises:
        ValueError: If the examples file cannot be loaded.
    """
    try:
        with open(examples_path, "r", encoding="utf-8") as file:
            examples = json.load(file)
        return examples
    except Exception as e:
        raise ValueError(f"Failed to load reference examples from {examples_path}: {str(e)}") from e

def tool_example_to_messages(examples: List[dict]) -> List[dict]:
    """
    Placeholder function to convert examples into the message format expected 
    by the LangChain runnable. For now, it performs an identity transformation.

    Args:
        examples (List[dict]): Raw example data.

    Returns:
        List[dict]: Processed example messages.
    """
    return examples

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
    raw_examples = load_reference_examples(examples_path)
    processed_examples = tool_example_to_messages(raw_examples)
    input_list = [{"text": chunk, "examples": processed_examples} for chunk in chunks]
    return input_list
