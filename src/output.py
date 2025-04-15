
import pandas as pd

def create_themes_dataframe(results):
    """
    Given a list of tuples (file_name, responses), where responses is a list of response dicts,
    each containing a 'themes' list, produce a Pandas DataFrame with columns:
      - 'Theme'
      - 'Matching Quotes'
      - 'Frequency'

    Args:
        results (list): List of tuples (file_name, responses), where responses is a list of dicts.

    Returns:
        pd.DataFrame: Aggregated DataFrame of themes and matching quotes across all files.
    """
    rows = []
    for file_name, responses in results:
        for response in responses:
            # Convert pydantic model to dict if needed
            if hasattr(response, "model_dump"):
                response = response.model_dump()
            theme_items = response.get("themes", [])
            for t in theme_items:
                rows.append({
                    "Theme": t["theme"],
                    "Matching Quotes": t["matching_quotes"]
                })

    df = pd.DataFrame(rows)

    grouped_data = []
    for theme, group in df.groupby("Theme"):
        all_quotes = "\n".join(group["Matching Quotes"].tolist())
        quotes_list = [quote.strip() for quote in all_quotes.split("\n") if quote.strip()]
        count = len(quotes_list)
        grouped_data.append({
            "Theme": theme,
            "Matching Quotes": all_quotes,
            "Frequency": count
        })

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
