import streamlit as st                                                                                                                                               
import sys                                                                                                                                              
import os          
import src.file_processor as fp
from src.data_model import aggregate_results
import pandas as pd                                                                                                                                     
                                                                                                                                                        
# Add the project root directory to the Python path                                                                                                     
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))                                                                           
if project_root not in sys.path:                                                                                                                        
    sys.path.insert(0, project_root)


def main():
    st.title("Theme Extraction Application")
    st.write("Welcome to the Theme Extraction Application! This application extracts themes from uploaded text files using LangChain and OpenAI.")
    
    uploaded_files = st.file_uploader("Upload text files", type="txt", accept_multiple_files=True)
    if uploaded_files:
        valid_files = []
        for uploaded_file in uploaded_files:
            if uploaded_file.size > 5 * 1024 * 1024:
                st.error(f"{uploaded_file.name} exceeds the size limit of 5MB")
            else:
                valid_files.append(uploaded_file)
        if valid_files:
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
                aggregated_df = fp.create_themes_dataframe(results)
                st.write("Aggregated Results:")
                st.dataframe(aggregated_df)
    
    st.write("Identified Themes will appear here.")

if __name__ == "__main__":
    main()
