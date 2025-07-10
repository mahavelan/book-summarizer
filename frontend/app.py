import streamlit as st
import requests

st.set_page_config(page_title="📘 Book Summary Web App", layout="centered")
st.title("📘 Book Summary Web App")

# Upload file
uploaded_file = st.file_uploader("Upload Book File (PDF, DOCX, TXT):", type=["pdf", "doc", "docx", "txt"])

# Select summary type
summary_type = st.radio("Choose summary type:", ["Chapter Summary", "Topic Summary", "Book Concept"])

# Page range input for topic summary
page_range = ""
if summary_type == "Topic Summary":
    page_range = st.text_input("Enter page range (e.g., 5-10):")

if uploaded_file:
    st.success("✅ File uploaded successfully.")

    if st.button(f"Generate {summary_type}"):
        with st.spinner("Processing your file, please wait..."):

            try:
                # Map user-friendly labels to backend types
                summary_type_map = {
                    "Chapter Summary": "chapter",
                    "Topic Summary": "topic",
                    "Book Concept": "bookconcept"
                }

                data = {"type": summary_type_map[summary_type]}

                # Validate page range format for topic summary
                if data["type"] == "topic":
                    if not page_range or "-" not in page_range:
                        st.warning("⚠️ Please enter a valid page range like '2-5'.")
                        st.stop()
                    data["page_range"] = page_range

                # Send to your backend on Render
                response = requests.post(
                    "https://book-summarizer-27gm.onrender.com/summarize",
                    data=data,
                    files={"file": uploaded_file}
                )

                if response.status_code == 200:
                    result = response.json().get("result", "No summary found.")
                    st.text_area(f"{summary_type} Output:", value=result, height=400)
                else:
                    st.error("❌ Failed to get summary. Try again later.")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

else:
    st.info("⬆️ Please upload a book file to begin.")
