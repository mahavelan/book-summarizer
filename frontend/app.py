import streamlit as st
import requests

st.set_page_config(page_title="📘 Book Summary Web App", layout="centered")
st.title("📘 Book Summary Web App")

uploaded_file = st.file_uploader("Upload Book File (PDF, DOCX, TXT):", type=["pdf", "doc", "docx", "txt"])

# Fixed summary type mapping
summary_options = {
    "Chapter Summary": "chapter",
    "Topic Summary": "topic",
    "Book Concept": "bookconcept"
}
summary_type_display = st.radio("Choose summary type:", list(summary_options.keys()))
summary_type = summary_options[summary_type_display]

# Only ask page range for Topic Summary
page_range = ""
if summary_type_display == "Topic Summary":
    page_range = st.text_input("Enter page range (e.g., 5-10):")

if uploaded_file:
    st.success("✅ File uploaded successfully.")
    if st.button(f"Generate {summary_type_display}"):
        with st.spinner("Processing your file, please wait..."):
            try:
                data = {"type": summary_type}
                if summary_type == "topic" and page_range:
                    data["page_range"] = page_range

                response = requests.post(
                    "https://book-summarizer-27gm.onrender.com/summarize",
                    data=data,
                    files={"file": uploaded_file}
                )

                if response.status_code == 200:
                    result = response.json().get("result", "No summary found.")
                    st.text_area(f"{summary_type_display} Output:", value=result, height=400)
                else:
                    st.error("❌ Failed to get summary.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
else:
    st.info("⬆️ Please upload a book file to begin.")
