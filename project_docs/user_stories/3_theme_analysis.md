cat > project_docs/user_stories/3_theme_analysis_stories.md << 'EOF'
# User Stories for Theme Extraction Application

## Theme Analysis Feature

### US-3.1: Theme Extraction from Text Files
**As a** user  
**I want to** have themes automatically extracted from my uploaded text files  
**So that** I can understand the key topics present in my qualitative data

**Acceptance Criteria:**
- The system uses LangChain (v0.3.23) and OpenAI's GPT models to analyze text content
- The system extracts themes from text chunks using the codebook defined in the application
- Each theme identified is from the predefined codebook list
- For each theme, relevant supporting quotes are extracted from the text
- The extraction process follows the workflow established in workspace.ipynb
- The system handles batched processing of multiple text chunks
- The system maintains traceability between quotes and their source text

**Technical Notes:**
- Use the `init_chat_model` from LangChain to initialize the LLM (default: "gpt-4o-mini")
- Implement the `extract_chunks` function to divide text files into manageable chunks
- Use Pydantic models (`Theme` and `Data` classes) for structured data extraction
- Implement the prompt template with system instructions and few-shot examples
- Use LangChain's structured output functionality with function calling
- Process text chunks in batches to optimize API usage

### US-3.2: Theme Organization and Presentation
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

### US-3.3: Codebook Management
**As a** user  
**I want to** have my text analyzed against a comprehensive predefined codebook  
**So that** the theme extraction is consistent and aligned with qualitative research standards

**Acceptance Criteria:**
- The system uses the predefined codebook from workspace.ipynb
- The codebook contains all theme categories relevant to the analysis
- The LLM is instructed to only extract themes that match the codebook
- The system properly constrains theme extraction to the codebook items

**Technical Notes:**
- Implement the codebook as a Python list in the application
- Include the codebook in the system prompt for the LLM
- Use Pydantic's `Field` with `enum` parameter to restrict theme extraction to codebook items
- Ensure the codebook is accessible throughout the application for consistency

### US-3.4: Example-Based Learning for Theme Extraction
**As a** user  
**I want to** have the theme extraction system learn from examples  
**So that** the extraction quality is high and consistent with qualitative research practices

**Acceptance Criteria:**
- The system uses few-shot learning with example texts and their expected theme extractions
- Examples demonstrate proper theme identification and quote association
- The system applies the learned patterns to new text analysis
- The examples cover various theme types and text patterns

**Technical Notes:**
- Implement the `tool_example_to_messages` function to format examples for the LLM
- Create a set of high-quality examples that demonstrate proper theme extraction
- Include examples in the prompt template using the `MessagesPlaceholder`
- Structure examples to show multiple themes per text and multiple quotes per theme
EOF
