# frontend/app.py

import streamlit as st
import requests

st.set_page_config(page_title="📘 Book Summary Web App", layout="centered")

st.title("📘 Book Summary Web App")

uploaded_file = st.file_uploader("Upload Book File (PDF, DOCX):", type=["pdf", "doc", "docx"])

summary_type = st.radio("Choose summary type:", ["Chapter Summary", "Topic Summary", "Book Concept"])

if uploaded_file:
    st.success("✅ File uploaded successfully.")
    if st.button(f"Generate {summary_type}"):
        with st.spinner("Processing your file, please wait..."):
            try:
                data = {"type": summary_type.lower().replace(" ", "")}
                files = {"file": uploaded_file.getvalue()}
                response = requests.post("https://book-summarizer-27gm.onrender.com/summarize", data=data, files={"file": uploaded_file})
                if response.status_code == 200:
                    result = response.json().get("result", "No summary found.")
                    st.text_area(f"{summary_type} Output:", value=result, height=400)
                else:
                    st.error("❌ Failed to get summary.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
else:
    st.info("⬆️ Please upload a book file to begin.")
