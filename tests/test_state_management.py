import pytest
import pandas as pd
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.state_management import save_dataframe_to_state, get_dataframe_from_state

def create_test_dataframe():
    """Helper function to create a test DataFrame"""
    return pd.DataFrame({
        'Theme': ['Theme 1', 'Theme 2'],
        'Matching Quotes': ['Quote 1\nQuote 2', 'Quote 3'],
        'Frequency': [2, 1]
    })

def test_save_and_get_dataframe():
    """Test saving and retrieving a DataFrame from state"""
    # Create test data
    test_df = create_test_dataframe()
    
    # Save to state
    save_dataframe_to_state(test_df, 'test_key')
    
    # Retrieve from state
    retrieved_df = get_dataframe_from_state('test_key')
    
    # Verify the data is correctly retrieved
    assert isinstance(retrieved_df, pd.DataFrame)
    assert list(retrieved_df.columns) == ['Theme', 'Matching Quotes', 'Frequency']
    assert len(retrieved_df) == 2
    assert retrieved_df['Theme'].tolist() == ['Theme 1', 'Theme 2']
    assert retrieved_df['Frequency'].tolist() == [2, 1]
    assert retrieved_df['Matching Quotes'].iloc[0].count('\n') == 1

def test_get_nonexistent_dataframe():
    """Test retrieving a non-existent DataFrame from state"""
    df = get_dataframe_from_state('nonexistent_key')
    assert df is None

def test_save_none_dataframe():
    """Test saving None as DataFrame to state"""
    save_dataframe_to_state(None, 'test_key')
    retrieved_df = get_dataframe_from_state('test_key')
    assert retrieved_df is None 