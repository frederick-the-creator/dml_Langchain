
import pandas as pd

def create_themes_dataframe(responses):
    
    """
    Given a list of response dictionaries, each containing a 'themes' list,
    produce a Pandas DataFrame with two columns:
      - 'Theme'
      - 'Matching Quotes'

    Args:
        responses (list): A list of dictionaries or Pydantic-like objects
                          each containing a 'themes' key.

    Returns:
        pd.DataFrame: A DataFrame with all themes and matching quotes
                      aggregated across all responses.
    """
    
    # In case each response is still a pydantic model, convert to dict
    # You can skip this step if your responses are already dictionaries.
    responses = [resp.model_dump() if hasattr(resp, "model_dump") else resp for resp in responses]
    
    # 1. Collect rows from each response
    rows = []
    for response in responses:
        # If responses are Pydantic models, convert them with model_dump() if needed.
        theme_items = response.get("themes", [])
        for t in theme_items:
            rows.append({
                "Theme": t["theme"],
                "Matching Quotes": t["matching_quotes"]
            })
    
    # 2. Create a DataFrame from the collected rows
    df = pd.DataFrame(rows)
    
    # 3. Group by "Theme" and aggregate the matching quotes.
    grouped_data = []
    for theme, group in df.groupby("Theme"):
        # Join all matching quotes for the theme into one string (each separated by a newline)
        all_quotes = "\n".join(group["Matching Quotes"].tolist())
        # Split into individual quotes, strip whitespace, and ignore empty entries.
        quotes_list = [quote.strip() for quote in all_quotes.split("\n") if quote.strip()]
        count = len(quotes_list)
        grouped_data.append({
            "Theme": theme,
            "Matching Quotes": all_quotes,
            "Frequency": count
        })
    
    # 4. Convert the grouped data into a DataFrame.
    df_merged = pd.DataFrame(grouped_data, columns=["Theme", "Matching Quotes", "Frequency"])

    df_merged = df_merged.sort_values('Frequency', ascending=False)

    return df_merged



def reduce_matching_quotes(df, n):
    """
    Reduces the number of matching quotes for each theme in the DataFrame to at most n quotes.
    
    Each cell in the "Matching Quotes" column is expected to have quotes separated by newline characters.
    
    Args:
        df (pd.DataFrame): A DataFrame with columns "Theme" and "Matching Quotes".
        n (int): The maximum number of matching quotes to keep for each theme.
        
    Returns:
        pd.DataFrame: A new DataFrame with the "Matching Quotes" column updated to have at most n quotes per theme.
    """
    # Make a copy of the dataframe to avoid modifying the original one.
    df_reduced = df.copy()
    
    # Process the "Matching Quotes" for each row: split by newline, take first n lines, and join them back.
    df_reduced["Matching Quotes"] = df_reduced["Matching Quotes"].apply(
        lambda quotes: "\n".join(quotes.split("\n")[:n])
    )

    return df_reduced


def display_multiline_table(df):
    """
    Return a Pandas Styler object that renders the newlines within cells
    in a Jupyter Notebook (or another HTML display).
    
    Call `display(display_multiline(df))` in a Jupyter cell to see multiline quotes.
    """
    return df.style.set_properties(**{'white-space': 'pre-wrap'})