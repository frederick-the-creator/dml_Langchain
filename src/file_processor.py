import time
from langchain.chat_models import init_chat_model

def read_file(uploaded_file):
    """
    Reads the content of an uploaded file as text (UTF-8).
    Returns the text content.
    Raises a ValueError if:
     - The file is empty or contains only whitespace.
     - Decoding fails due to unsupported encoding.
    """
    try:
        file_bytes = uploaded_file.read()
        text = file_bytes.decode('utf-8')
        if not text.strip():
            raise ValueError(f"File '{uploaded_file.name}' is empty or contains only whitespace.")
        return text
    except UnicodeDecodeError as e:
        raise ValueError(f"Unsupported encoding in {uploaded_file.name}: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error reading {uploaded_file.name}: {str(e)}")

def chunk_text(text, lines_per_chunk=10):
    """
    Splits the text into chunks, each containing up to 'lines_per_chunk' lines.
    This is based on the chunking logic from the workspace notebook.
    """
    lines = text.splitlines()
    chunks = []
    for i in range(0, len(lines), lines_per_chunk):
        chunk = "\n".join(lines[i:i+lines_per_chunk]).strip()
        if chunk:
            chunks.append(chunk)
    return chunks

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

def process_file(file_content):
    """
    Processes file content for theme analysis by splitting the text into chunks,
    running them through a LangChain runnable, and aggregating the results.
    
    This implementation now:
      - Configures the prompt template with a structured output schema.
      - Initializes the LangChain model with error-handled API calls.
      - Processes text chunks in batches for API optimization.
    
    Returns:
        dict: A dictionary with keys "themes" and "quotes" as extracted by the LLM.
    
    Raises:
        ValueError: If an error occurs during processing.
    """
    # 1. Split text into manageable chunks.
    chunks = chunk_text(file_content, lines_per_chunk=10)
    
    # 2. Initialize the LLM using our error-handled utility function.
    llm = init_llm()
    
    # 3. Import the prompt template.
    try:
        from prompts import prompt_template
    except ImportError:
        raise ImportError("Could not import prompt_template from prompts.py. Please ensure it exists and is correct.")
    
    # 4. Build the input_list for batch processing.
    input_list = [{"text": chunk, "examples": []} for chunk in chunks]
    
    try:
        # 5. Configure the LangChain runnable.
        from data_model import Data  # Ensure this path is correct.
        runnable = prompt_template | llm.with_structured_output(
            schema=Data,
            method="function_calling",
            include_raw=False
        )
        
        # 6. Process the input list using batch mode.
        responses = runnable.batch(input_list)
        
        # 7. Aggregate the outputs.
        aggregated_themes = []
        aggregated_quotes = []
        for response in responses:
            aggregated_themes.extend(response.get("themes", []))
            aggregated_quotes.extend(response.get("quotes", []))
            
        return {"themes": aggregated_themes, "quotes": aggregated_quotes}
    except Exception as e:
        raise ValueError(f"Error processing file content: {str(e)}")
