import streamlit as st
import pandas as pd

def save_dataframe_to_state(df: pd.DataFrame, key: str) -> None:
    """
    Save a DataFrame to Streamlit's session state.
    
    Args:
        df: The DataFrame to save
        key: The key to store the DataFrame under
    """
    if df is not None and not df.empty:
        st.session_state[key] = df
    else:
        # If df is None or empty, remove the key from session state if it exists
        st.session_state.pop(key, None)

def get_dataframe_from_state(key: str) -> pd.DataFrame:
    """
    Retrieve a DataFrame from Streamlit's session state.
    
    Args:
        key: The key under which the DataFrame is stored
        
    Returns:
        The stored DataFrame or None if not found
    """
    return st.session_state.get(key) 