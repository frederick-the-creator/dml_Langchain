import pandas as pd

def import_themes_from_csv(file):
    """
    Import themes from a CSV file and return them as a pandas DataFrame.
    
    Args:
        file: A file-like object containing CSV data
        
    Returns:
        pd.DataFrame: DataFrame containing the imported themes
        
    Raises:
        ValueError: If the CSV file doesn't have the required columns
    """
    try:
        df = pd.read_csv(file)
        required_columns = ['Theme', 'Matching Quotes', 'Frequency']
        
        # Check if all required columns are present
        if not all(col in df.columns for col in required_columns):
            raise ValueError("CSV must contain required columns: Theme, Matching Quotes, Frequency")
            
        # Ensure columns are in the correct order
        df = df[required_columns]
        
        return df
    except pd.errors.EmptyDataError:
        # Return empty DataFrame with correct structure if file is empty
        return pd.DataFrame(columns=required_columns)
    except Exception as e:
        raise ValueError(f"Error importing CSV: {str(e)}") 