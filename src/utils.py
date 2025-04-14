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
