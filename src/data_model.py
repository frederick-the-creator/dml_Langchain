from typing import List
from pydantic import BaseModel

class FileThemeData(BaseModel):
    """
    Data model to represent the theme extraction result for a file.
    
    Attributes:
      source_file: The name of the source file.
      themes: List of themes extracted from the file.
      quotes: List of quotes associated with each theme.
    """
    source_file: str
    themes: List[str]
    quotes: List[str]

def aggregate_results(results: List[tuple]) -> List[FileThemeData]:
    """
    Converts a list of tuples (source_file, result_dict) into a list of FileThemeData instances.
    
    Args:
        results: List of tuples, where each tuple contains:
            - source_file (str): The name of the source file.
            - result_dict: A dictionary with keys "themes" and "quotes".
    
    Returns:
        List[FileThemeData]: Aggregated data for all processed files.
    """
    aggregated = []
    for source_file, result in results:
        data = FileThemeData(
            source_file=source_file,
            themes=result.get("themes", []),
            quotes=result.get("quotes", [])
        )
        aggregated.append(data)
    return aggregated
