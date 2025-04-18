import streamlit as st                                                                                                                                               
import sys                                                                                                                                              
import os                                                                                                                                          
                                                                                                                                                        
# Add the project root directory to the Python path                                                                                                     
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))                                                                           
if project_root not in sys.path:                                                                                                                        
    sys.path.insert(0, project_root)

import src.file_processor as fp
from src.data_model import aggregate_results
from src.output import create_themes_dataframe, reduce_matching_quotes, display_multiline_table
from src.csv_operations import import_themes_from_csv
from src.state_management import save_dataframe_to_state, get_dataframe_from_state

def main():
    st.title("Theme Extraction Application")
    st.write("Welcome to the Theme Extraction Application! This application extracts themes from uploaded text files using LangChain and OpenAI.")
    
    # Initialize session state for storing results
    if 'processed_results' not in st.session_state:
        st.session_state.processed_results = None
    
    uploaded_files = st.file_uploader(
        "Upload text, CSV, or PDF files",
        type=["txt", "csv", "pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        valid_files = uploaded_files
        st.write("Uploaded files:")
        for uploaded_file in valid_files:
            st.write(uploaded_file.name)
        st.success("Files uploaded successfully")
        if st.button("Process Files"):
            with st.spinner("Processing files..."):
                results = []
                total_files = len(valid_files)
                progress_bar = st.progress(0)
                for idx, uploaded_file in enumerate(valid_files):
                    try:
                        content = fp.read_file(uploaded_file)
                        result = fp.process_file(content)
                        results.append((uploaded_file.name, result))
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {e}")
                    progress_bar.progress((idx+1)/total_files)
            st.success("Processing complete")
            full_df = create_themes_dataframe(results)
            reduced_df = reduce_matching_quotes(full_df, 3)
            save_dataframe_to_state(reduced_df, 'processed_results')
            save_dataframe_to_state(full_df, 'full_results')

    # Display processed results if they exist
    reduced_df = get_dataframe_from_state('processed_results')
    if reduced_df is not None:
        st.markdown("## Theme Extracted from Raw Data", unsafe_allow_html=True)
        st.dataframe(reduced_df)
        
        # Add download button for the full CSV export
        full_df = get_dataframe_from_state('full_results')
        csv = full_df.to_csv(index=False)
        st.download_button(
            label="Download Themes as CSV",
            data=csv,
            file_name="full_themes.csv",
            mime="text/csv"
        )

    # Add CSV import section
    st.markdown("---")
    uploaded_csv = st.file_uploader("Upload edited themes CSV", type="csv", accept_multiple_files=False)
    if uploaded_csv is not None:
        try:
            imported_df = import_themes_from_csv(uploaded_csv)
            st.markdown("## Themes Updated by User", unsafe_allow_html=True)
            st.dataframe(imported_df)
        except ValueError as e:
            st.error(str(e))

if __name__ == "__main__":
    main()
