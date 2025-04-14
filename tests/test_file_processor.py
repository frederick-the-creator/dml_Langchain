import io                                                                                                                                                                           
import pytest

import sys                                                                                                                                              
import os                                                                                                                                               
                                                                                                                                                        
# Add the project root directory to the Python path                                                                                                     
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))                                                                           
if project_root not in sys.path:                                                                                                                        
    sys.path.insert(0, project_root)


from src.file_processor import chunk_text                                                                                                                                           
                                                                                                                                                                                    
def test_chunk_text_exact_division():                                                                                                                                               
    # Create a test string with exactly 20 lines                                                                                                                                    
    test_text = "\n".join([f"Line {i}" for i in range(1, 21)])                                                                                                                      
    # Using lines_per_chunk=10, this should create 2 chunks                                                                                                                         
    chunks = chunk_text(test_text, lines_per_chunk=10)                                                                                                                              
    assert len(chunks) == 2                                                                                                                                                         
    # Check that the first chunk starts with "Line 1" and ends with "Line 10"                                                                                                       
    assert chunks[0].startswith("Line 1")                                                                                                                                           
    assert "Line 10" in chunks[0]                                                                                                                                                   
                                                                                                                                                                                    
def test_chunk_text_remainder():                                                                                                                                                    
    # Create a text with 15 lines; expect chunks: 10 lines and 5 lines                                                                                                              
    test_text = "\n".join([f"Line {i}" for i in range(1, 16)])                                                                                                                      
    chunks = chunk_text(test_text, lines_per_chunk=10)                                                                                                                              
    assert len(chunks) == 2                                                                                                                                                         
    # The second chunk should have 5 lines, verify by splitting it:                                                                                                                 
    assert len(chunks[1].splitlines()) == 5

from src.file_processor import read_file                                                                                                                                            
                                                                                                                                                                                    
def test_read_file_valid_utf8():                                                                                                                                                    
    content = "This is valid utf-8 content."                                                                                                                                        
    file_mock = io.BytesIO(content.encode('utf-8'))                                                                                                                                 
    # Give the BytesIO object a name attribute similar to an uploaded file.                                                                                                         
    file_mock.name = "valid.txt"                                                                                                                                                    
    result = read_file(file_mock)                                                                                                                                                   
    assert result == content                                                                                                                                                        
                                                                                                                                                                                    
def test_read_file_empty_file():                                                                                                                                                    
    content = ""                                                                                                                                                                    
    file_mock = io.BytesIO(content.encode('utf-8'))                                                                                                                                 
    file_mock.name = "empty.txt"                                                                                                                                                    
    with pytest.raises(ValueError) as excinfo:                                                                                                                                      
        read_file(file_mock)                                                                                                                                                        
    assert "empty" in str(excinfo.value).lower()                                                                                                                                    
                                                                                                                                                                                    
def test_read_file_invalid_encoding():                                                                                                                                              
    # Create a file with invalid UTF-8 bytes.                                                                                                                                       
    file_mock = io.BytesIO(b"\xff")                                                                                                                                                 
    file_mock.name = "invalid.txt"                                                                                                                                                  
    with pytest.raises(ValueError) as excinfo:                                                                                                                                      
        read_file(file_mock)                                                                                                                                                        
    assert "unsupported encoding" in str(excinfo.value).lower() or "utf-8" in str(excinfo.value)  