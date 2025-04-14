from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.utils import load_codebook

codebook = load_codebook()

# Build the prompt template.
# The system message now includes detailed instructions and dynamically inserts the codebook list.
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert qualitative research algorithm. You are given a text to code deductively using a list of codes.\n"
            "Your job is to extract the themes from the text and their associated quotes. Each quote can have multiple themes and each theme can have multiple quotes.\n"
            f"You can only extract themes that belong to this list {str(codebook)}"
        ),
        MessagesPlaceholder("examples"),
        ("human", "{text}"),
    ]
)
