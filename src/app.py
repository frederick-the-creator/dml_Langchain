import streamlit as st

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
                st.info("Processing will be implemented in future stories")
    
    st.write("Identified Themes will appear here.")

if __name__ == "__main__":
    main()
