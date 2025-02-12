import streamlit as st
from src.anonymizer import PDFAnonymizer
from src.utils import anonymize_text, format_found_items, get_embeddings_json

def main():
    # Page configuration
    st.set_page_config(
        page_title="PDF Anonymizer",
        page_icon="📄",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .stButton > button {
            background-color: #FF4B4B;
            color: white;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            border: none;
        }
        .success {
            color: #09AB3B;
        }
        .container {
            padding: 1.5rem;
        }
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 10px;
            background-color: #0E1117;
            border-top: 1px solid #1E1E1E;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.title("📄 PDF Anonymizer")
    st.markdown("""
        Upload your PDF documents to automatically anonymize sensitive information.
        The tool will mask personal data like emails, phone numbers, and addresses.
    """)

    # File upload - now supports multiple files
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True,
        help="Upload one or more PDF files to begin the anonymization process"
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.subheader(f"Processing: {uploaded_file.name}")
            try:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    # Extract text from PDF
                    pdf_text = PDFAnonymizer.extract_text(uploaded_file)

                    # Anonymize the text
                    anonymized_text, found_items, embeddings_data = anonymize_text(pdf_text)

                    # Display results in columns
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Original Content")
                        st.text_area(
                            "Original text",
                            pdf_text,
                            height=300,
                            disabled=True,
                            key=f"original_{uploaded_file.name}"
                        )

                    with col2:
                        st.subheader("Anonymized Content")
                        st.text_area(
                            "Anonymized text",
                            anonymized_text,
                            height=300,
                            disabled=True,
                            key=f"anonymized_{uploaded_file.name}"
                        )

                    # Display found sensitive information
                    st.subheader("Detected Sensitive Information")
                    st.code(format_found_items(found_items))

                    # Create download buttons
                    col3, col4 = st.columns(2)
                    with col3:
                        # Create download button for anonymized PDF
                        anonymized_pdf = PDFAnonymizer.create_anonymized_pdf(anonymized_text)
                        st.download_button(
                            label="Download Anonymized PDF",
                            data=anonymized_pdf,
                            file_name=f"anonymized_{uploaded_file.name}",
                            mime="application/pdf",
                            key=f"pdf_{uploaded_file.name}"
                        )

                    with col4:
                        # Create download button for embeddings
                        embeddings_json = get_embeddings_json(embeddings_data)
                        st.download_button(
                            label="Download Embeddings",
                            data=embeddings_json,
                            file_name=f"embeddings_{uploaded_file.name}.json",
                            mime="application/json",
                            key=f"json_{uploaded_file.name}"
                        )

            except Exception as e:
                st.error(f"An error occurred processing {uploaded_file.name}: {str(e)}")

    # Footer
    st.markdown(
        """
        <div class="footer">
            Created by <a href="https://edujbarrios.com" target="_blank">edujbarrios.com</a>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()