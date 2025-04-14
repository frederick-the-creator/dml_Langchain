from typing import Optional, List
from pydantic import BaseModel, Field
from src.utils import load_codebook

CODEBOOK = load_codebook()

class Theme(BaseModel):
    """
    Pydantic model representing a theme identified in the text.

    Attributes:
      theme: The name of the theme, restricted to the allowed values from the codebook.
      matching_quotes: Aggregated quotes supporting this theme, each separated by a newline.
    """
    theme: Optional[str] = Field(
        default=None,
        description="Name of the theme identified",
        enum=CODEBOOK
    )
    matching_quotes: Optional[str] = Field(
        default=None,
        description="All quotes from the text that match the identified theme, each on a new line."
    )

class Data(BaseModel):
    """
    Pydantic model for encapsulating extracted themes data from text.

    Attributes:
      themes: A list of Theme instances representing the themes extracted from the text.
    """
    themes: List[Theme]

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
