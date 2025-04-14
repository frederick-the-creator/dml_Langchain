import os
import json

def load_codebook():
    """
    Loads the codebook from 'codebook.json' located in the same directory as this module.
    
    Returns:
        list: The list of allowed codes.
        
    Raises:
        ValueError: If the codebook cannot be loaded.
    """
    codebook_path = os.path.join(os.path.dirname(__file__), "codebook.json")
    try:
        with open(codebook_path, "r", encoding="utf-8") as f:
            codebook = json.load(f)
        return codebook
    except Exception as e:
        raise ValueError(f"Failed to load codebook from {codebook_path}: {str(e)}")

def init_llm():
    """
    Initializes and returns the LangChain LLM using the provided
    model identifier and model_provider.
    
    Raises:
        ValueError: If the LLM initialization fails.
    """
    from langchain.chat_models import init_chat_model
    try:
        llm = init_chat_model("gpt-4o-mini", model_provider="openai")
        return llm
    except Exception as e:
        raise ValueError(f"Failed to initialize the LangChain LLM: {str(e)}")
