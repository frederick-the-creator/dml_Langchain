import time
from langchain.chat_models import init_chat_model
from src.utils import init_llm
from src.prompts import prompt_template
from src.data_model import Data
from src.input import create_input_list
from langchain.document_loaders import PyPDFLoader
import os


def read_file(uploaded_file):
    """
    Reads the content of an uploaded file as text (UTF-8) or PDF.
    Returns the text content.
    Raises a ValueError if:
     - The file is empty or contains only whitespace.
     - Decoding fails due to unsupported encoding.
     - PDF extraction fails or file is not a valid PDF.
    """
    filename = getattr(uploaded_file, 'name', '')
    ext = os.path.splitext(filename)[1].lower()
    try:
        if ext == '.pdf':
            # Save PDF to a temporary file for LangChain loader
            import tempfile
            with tempfile.NamedTemporaryFile(delete=True, suffix='.pdf') as tmp:
                tmp.write(uploaded_file.read())
                tmp.flush()
                try:
                    loader = PyPDFLoader(tmp.name)
                    docs = loader.load()
                    text = "\n".join([doc.page_content for doc in docs])
                except Exception as e:
                    raise ValueError(f"Error reading PDF {filename}: {str(e)}")
            if not text.strip():
                raise ValueError(f"PDF '{filename}' is empty or contains only whitespace.")
            return text
        else:
            file_bytes = uploaded_file.read()
            text = file_bytes.decode('utf-8')
            if not text.strip():
                raise ValueError(f"File '{filename}' is empty or contains only whitespace.")
            return text
    except UnicodeDecodeError as e:
        raise ValueError(f"Unsupported encoding in {filename}: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error reading {filename}: {str(e)}")

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
    
    # 4. Build the input_list for batch processing.
    input_list = create_input_list(chunks)
    
    try:
        # 5. Configure the LangChain runnable.
        runnable = prompt_template | llm.with_structured_output(
            schema=Data,
            method="function_calling",
            include_raw=False
        )
        
        # 6. Process the input list using batch mode.
        responses = runnable.batch(input_list)

        return responses
    except Exception as e:
        raise ValueError(f"Error processing file content: {str(e)}")