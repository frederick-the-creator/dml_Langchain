import pytest

import sys                                                                                                                                              
import os                                                                                                                                               
                                                                                                                                                        
# Add the project root directory to the Python path                                                                                                     
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))                                                                           
if project_root not in sys.path:                                                                                                                        
    sys.path.insert(0, project_root)

from src.data_model import aggregate_results, FileThemeData                                                                                                                         
                                                                                                                                                                                    
def test_aggregate_results():                                                                                                                                                       
    # Prepare dummy inputs                                                                                                                                                          
    results = [                                                                                                                                                                     
        ("file1.txt", {"themes": ["dummy_theme", "dummy_theme"], "quotes": ["quote1", "quote2"]}),                                                                                  
        ("file2.txt", {"themes": ["dummy_theme", "dummy_theme", "dummy_theme"], "quotes": ["quote3", "quote4", "quote5"]}),                                                         
    ]                                                                                                                                                                               
    aggregated = aggregate_results(results)                                                                                                                                         
    # Check aggregated results length equals number of input files.                                                                                                                 
    assert len(aggregated) == 2                                                                                                                                                     
                                                                                                                                                                                    
    # Verify contents for file1.txt                                                                                                                                                 
    file1_data = next(item for item in aggregated if item.source_file == "file1.txt")                                                                                               
    assert file1_data.themes == ["dummy_theme", "dummy_theme"]                                                                                                                      
    assert file1_data.quotes == ["quote1", "quote2"]                                                                                                                                
                                                                                                                                                                                    
    # Verify contents for file2.txt                                                                                                                                                 
    file2_data = next(item for item in aggregated if item.source_file == "file2.txt")                                                                                               
    assert len(file2_data.themes) == 3                                                                                                                                              
    assert len(file2_data.quotes) == 3