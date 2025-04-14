from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# A minimal prompt template used as a placeholder for theme extraction.
# It includes:
#   - A system message setting the context.
#   - A placeholder for examples.
#   - A human message for the text chunk.
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert qualitative research algorithm. Your job is to extract themes and associated quotes from the provided text."),
    MessagesPlaceholder("examples"),
    ("human", "{text}")
])
