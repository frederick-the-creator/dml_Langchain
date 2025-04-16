import pytest
import pandas as pd
import io
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.csv_operations import import_themes_from_csv

def create_test_csv():
    """Helper function to create a test CSV file-like object"""
    test_data = {
        'Theme': ['Theme 1', 'Theme 2'],
        'Matching Quotes': ['Quote 1\nQuote 2', 'Quote 3'],
        'Frequency': [2, 1]
    }
    df = pd.DataFrame(test_data)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return csv_buffer

def test_import_themes_from_csv():
    """Test importing themes from a CSV file"""
    # Create a test CSV file
    test_csv = create_test_csv()
    
    # Test importing the CSV
    imported_df = import_themes_from_csv(test_csv)
    
    # Verify the dataframe structure
    assert isinstance(imported_df, pd.DataFrame)
    assert list(imported_df.columns) == ['Theme', 'Matching Quotes', 'Frequency']
    
    # Verify the data
    assert len(imported_df) == 2
    assert imported_df['Theme'].tolist() == ['Theme 1', 'Theme 2']
    assert imported_df['Frequency'].tolist() == [2, 1]
    assert imported_df['Matching Quotes'].iloc[0].count('\n') == 1  # Check if multiline quotes are preserved

def test_import_themes_from_invalid_csv():
    """Test importing themes from an invalid CSV file"""
    # Create an invalid CSV
    invalid_csv = io.StringIO('Invalid,CSV\nData,Format')
    
    # Test that it raises an appropriate error
    with pytest.raises(ValueError, match="CSV must contain required columns"):
        import_themes_from_csv(invalid_csv)

def test_import_themes_from_empty_csv():
    """Test importing themes from an empty CSV file"""
    # Create an empty CSV with correct headers
    empty_csv = io.StringIO('Theme,Matching Quotes,Frequency\n')
    
    # Test importing the empty CSV
    imported_df = import_themes_from_csv(empty_csv)
    
    # Verify we get an empty dataframe with correct structure
    assert isinstance(imported_df, pd.DataFrame)
    assert list(imported_df.columns) == ['Theme', 'Matching Quotes', 'Frequency']
    assert len(imported_df) == 0 