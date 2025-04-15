import os
import json
from langchain.chat_models import init_chat_model

def load_json_data(filepath: str = None):
    """
    Loads JSON data from the specified filepath. If no filepath is provided,
    it defaults to loading 'codebook.json' located in the same directory as this module.
    
    Args:
        filepath (str, optional): Path to the JSON file. Defaults to None.
    
    Returns:
        Any: The JSON data loaded from the file.
        
    Raises:
        ValueError: If the file cannot be loaded.
    """

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise ValueError(f"Failed to load JSON data from {filepath}: {str(e)}")

def init_llm():
    """
    Initializes and returns the LangChain LLM using the provided
    model identifier and model_provider.
    
    Raises:
        ValueError: If the LLM initialization fails.
    """
    try:
        llm = init_chat_model("gpt-4o-mini", model_provider="openai")
        return llm
    except Exception as e:
        raise ValueError(f"Failed to initialize the LangChain LLM: {str(e)}")
