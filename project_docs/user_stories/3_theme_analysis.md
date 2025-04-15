cat > project_docs/user_stories/3_theme_analysis_stories.md << 'EOF'
# User Stories for Theme Extraction Application

## Theme Analysis Feature

### US-3.1: Core Theme Extraction Functions from Text Files
**As a** user  
**I want to** 
- Implement the core LangChain runnable functions from workspace.ipynb in the appropriate file / function in the web application (e.g. process_file())
- Ensure all required inputs to the runnable are passed to it from an appropriate location (e.g. prompt_template, llm.with_structured_ouptut, input_list, pytdantic Data model). You do not have to fully define and implement all these inputs, just define in which files / functions they will belong and create placeholder functions and dummy values. 
- Ensure that the environment variables are correctly loaded and the LangChain model is initialised as llm in the appropriate file / function in the web application so it can be passed to the runnable function as llm.with_structured_output.


**Acceptance Criteria**
- Implement the core LangChain runnable functions from workspace.ipynb in the process_file() functio
- Ensure the runnable is properly configured with the prompt template, LLM, and structured output schema
- Load environment variables correctly for OpenAI API access
- Initialize the LangChain model as llm using init_chat_model("gpt-4o-mini", model_provider="openai")
- Process text chunks in batches to optimize API usage
- Return structured theme data that can be used by downstream visualization functions

**Technical Notes**
- Use LangChain version compatible with function calling (langchain-core ≥ 0.1.0)
The runnable should follow this pattern: prompt_template | llm.with_structured_output(schema=Data, method="function_calling", include_raw=False)
- Environment variables needed: OPENAI_API_KEY, LANGSMITH_API_KEY (optional), LANGSMITH_PROJECT (optional)
- Store the LLM initialization in a separate utility function for reusability
- The function should handle errors gracefully, especially API-related issues


### US-3.2: Creating Inputs - Prompt Template
**As a** user  
**I want to** 
- Implement prompt template from workspace.ipynb in the appropriate file / function in the web application so that it feeds the LangChain runnable
- The prompt template should take the codebook as input, which should be stored separate from the code to allow for easy updates and changes

**Acceptance Criteria**
- Implement the prompt template from workspace.ipynb in a dedicated module (e.g., prompts.py)
- Store the codebook in a separate JSON or YAML file for easy updates
- Load the codebook dynamically when creating the prompt template
- Use ChatPromptTemplate with system and human messages
- Include the MessagesPlaceholder for examples in the template
- Ensure the prompt clearly instructs the model to extract themes from the provided codebook only

**Technical Notes**
- Use langchain_core.prompts.ChatPromptTemplate and MessagesPlaceholder
- The system message should use the exact same text as in workspace.ipynb
- The prompt should explicitly include the codebook list in the system message



### US-3.3: Creating Inputs - Pydantic Data Model
**As a** user  
**I want to** 
- Implement the Pydantic Data Model from workspace.ipynb in the appropriate file / function in the web application so that it feeds the LangChain runnable (e.g. data_model.py)
- Ensure this is being called by the main Langchain runnable function

**Acceptance Criteria:**
- Implement the Pydantic Data Model in a dedicated module (e.g., data_model.py)
- Create a Theme class matching exactly the class in workspace.ipynb
- Create a Data class matching exactly the class in workspace.ipynb
- Ensure the theme field uses the codebook as an enum to restrict values
- Make fields optional with appropriate default values
- Include descriptive docstrings for each class and field

**Technical Notes**
- Import the codebook from the same source used by the prompt template
- The Classes implemented should be exactly the same as in workspace.ipynb


### US-3.4: Creating Inputs - Input List
**As a** user  
**I want to** 
- Implement the input_list from workspace.ipynb in the appropriate file / function in the web application so that it feeds the LangChain runnable
- The input list should be created by combining the chunks from the text files uploaded by the user with the reference examples 
- The reference examples (found in the examples list of workspace.ipynb) should be stored separate from the code in a structured manner and read in to allow for easy updates and changes. They should be passed to the tool_example_to_messages() function as per workspace.ipynb
- Any other supporting inputs or functions should also be implemented (e.g. the Pydantica Data Model is used by tool_example_to_messages())


**Acceptance Criteria:**
- Implement the input_list creation function in the appropriate module (e.g., input_list.py)
- Store reference examples in a JSON or YAML file separate from the code
- Load and process examples using the tool_example_to_messages() function
- Combine text chunks with reference examples to create the complete input list
- Format each input as a dictionary with "text" and "examples" keys

**Techical Notes**
- Use the tool_example_to_messages() function from LangChain to format examples
- Store examples in this format
examples = [
    (
        "Text content...",
        Data(themes=[Theme(...), Theme(...)])
    )
- Input list should be structured as
   - input_list = [{"text": chunk, "examples": messages} for chunk in input_texts]
- Handle any LangChain beta warnings appropriately
- Ensure the Data and Theme classes are imported correctly


### US-3.5: Theme Organization and Presentation
**As a** user  
**I want to** see the extracted themes organized with their supporting quotes  
**So that** I can easily review and understand the thematic analysis of my data

**Acceptance Criteria:**
- Themes are presented in a structured format matching the output in workspace.ipynb
- Themes are sorted by frequency of occurrence
- Each theme displays its associated quotes
- The system aggregates quotes for the same theme across different text chunks
- The presentation allows for easy scanning of themes and exploration of supporting evidence
- The output can be viewed in the web interface

**Technical Notes:**
- Use pandas (v2.2.3) for data organization and manipulation
- Implement the `create_themes_dataframe` function to collect and organize themes
- Use the `reduce_matching_quotes` function to manage display of large quote collections
- Format the display to handle multi-line text properly
- Calculate and display frequency metrics for each theme
- Ensure the UI can render the structured data in a readable format