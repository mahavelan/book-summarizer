import streamlit as st
import requests

st.set_page_config(page_title="📘 Book Summary Web App", layout="centered")

st.title("📘 Book Summary Web App")

uploaded_file = st.file_uploader("Upload Book File (PDF, DOCX, TXT, etc):", type=None)

summary_type = st.radio("Choose summary type:", ["Chapter", "Topic", "Book Concept"])

page_range = ""
if summary_type == "Topic":
    page_range = st.text_input("Enter page range (e.g., 5-10):")

if uploaded_file:
    st.success("✅ File uploaded successfully.")
    if st.button(f"Generate {summary_type}"):
        with st.spinner("Processing your file, please wait..."):
            try:
                files = {"file": uploaded_file.getvalue()}
                data = {"type": summary_type.lower().replace(" ", "")}

                if summary_type == "Topic" and page_range:
                    data["page_range"] = page_range

                response = requests.post("http://localhost:8000/summarize", files={"file": uploaded_file}, data=data)

                if response.status_code == 200:
                    result = response.json().get("result", "No summary found.")
                    st.text_area(f"{summary_type} Output:", value=result, height=400)
                else:
                    st.error("❌ Failed to get summary. Please try again.")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
else:
    st.info("⬆️ Please upload a book file to begin.")
