import time

def read_file(uploaded_file):
    """
    Reads the content of an uploaded file as text (UTF-8).
    Returns the text content or raises an exception if decoding fails.
    """
    try:
        file_bytes = uploaded_file.read()
        return file_bytes.decode('utf-8')
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

def process_file(file_content):
    """
    Processes file content for theme analysis by chunking the text
    and simulating LLM processing on each chunk.
    """
    chunks = chunk_text(file_content, lines_per_chunk=10)
    aggregated_themes = []
    aggregated_quotes = []
    for chunk in chunks:
        # Simulate processing time for each chunk
        for _ in range(10):
            time.sleep(0.005)
        # Dummy extraction: for demonstration, assign a fixed theme and use a portion of the chunk as a sample quote.
        aggregated_themes.append("dummy_theme")
        aggregated_quotes.append(chunk[:50])
    return {"themes": aggregated_themes, "quotes": aggregated_quotes}
