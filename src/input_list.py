from typing import List, Dict
from src.file_processor import chunk_text
from src.utils import load_json_data
from langchain_core.utils.function_calling import tool_example_to_messages

examples = [
    (
        # Full text with all sentences and formatting removed:
        "Can we use empty buildings as new spaces for democratic decision-making.\n"
        "Big businesses in Sheffield.... very few.\n"
        "Local politicians engage relatively well where they live... but uninformed about transversal themes (mental health/food).\n"
        "In the age of disinformation, how can we build trust at a community level... build fertile ground for collective action.\n"
        "City leadership and fellow citizens have come out of a rough patch - tree felling.\n"
        "Innovative leadership and transparent decision-making inspire public trust and foster robust community participation.\n"
        "Local area committees are good but not fully started yet.\n"
        "Humans, not organisations make the difference - humans with resources that happen to be within organisations.\n"
        "You have to invest to enable people to be heard... and processes need to be genuine and influence decision making.\n"
        "What if every decision was made with young people/the next generation in mind.\n"
        "How can decisions be announced in a more distributed way... not just at city hall.",
        
        # Structured data with themes and their matching quotes:
        Data(themes=[
            Theme(
                theme="Governance and Civic Engagement",
                matching_quotes="Can we use empty buildings as new spaces for democratic decision-making."
            ),
            Theme(
                theme="Social Equity and Inclusion",
                matching_quotes="Local politicians engage relatively well where they live... but uninformed about transversal themes (mental health/food)."
            ),
            Theme(
                theme="Trust & Relationships",
                matching_quotes="In the age of disinformation, how can we build trust at a community level... build fertile ground for collective action.\n"
                                "Innovative leadership and transparent decision-making inspire public trust and foster robust community participation."
            ),
            Theme(
                theme="Community Engagement & Participation",
                matching_quotes=(
                    "In the age of disinformation, how can we build trust at a community level... build fertile ground for collective action.\n"
                    "You have to invest to enable people to be heard... and processes need to be genuine and influence decision making.\n"
                    "Innovative leadership and transparent decision-making inspire public trust and foster robust community participation."
                )
            ),
            Theme(
                theme="Community Spaces and Facilities",
                matching_quotes="Humans, not organisations make the difference - humans with resources that happen to be within organisations."
            ),
            Theme(
                theme="Youth Engagement & Future Focus",
                matching_quotes="What if every decision was made with young people/the next generation in mind."
            ),
            Theme(
                theme="Communication & Information",
                matching_quotes="How can decisions be announced in a more distributed way... not just at city hall."
            ),
            Theme(
                theme="Leadership & Governance",
                matching_quotes=(
                    "City leadership and fellow citizens have come out of a rough patch - tree felling.\n"
                    "Innovative leadership and transparent decision-making inspire public trust and foster robust community participation."
                )
            ),
        ])
    ),
    # (
    #     """Local area committees are good but not fully started yet.""",
    #     Data(themes=[]),
    # )
]






def create_input_list(chunks: List[str], examples: List[dict]) -> List[Dict[str, any]]:
    """
    Creates the input list for the LangChain runnable by attaching processed reference examples
    to each provided text chunk.

    Args:
        chunks (List[str]): A list of text chunks.
        examples_path (str): Path to the JSON file containing reference examples.

    Returns:
        List[Dict[str, any]]: A list of dictionaries where each dictionary has:
            - "text": A text chunk.
            - "examples": The processed reference examples.
    """

    messages = []

    for text, tool_call in examples:
        messages.extend(
            tool_example_to_messages(text, [tool_call])
        )

    input_list = [{"text": chunk, "examples": messages} for chunk in chunks]
    return input_list
