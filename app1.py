import streamlit as st
import pdfplumber
import re

st.title("📄 Document Analyzer (Resume / PDF)")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"

    st.subheader("Extracted Text")
    st.text(text[:1000])

    st.subheader("Quick Insights")

    # Simple keyword extraction
    skills = re.findall(r"Python|SQL|Power BI|HTML|CSS|Machine Learning|Data Science", text, re.I)
    education = re.findall(r"Bachelor|Engineering|University|HSC|SSC", text, re.I)
    projects = re.findall(r"Project|System|Application|Platform", text, re.I)

    col1, col2, col3 = st.columns(3)
    col1.metric("Skills Found", len(set(skills)))
    col2.metric("Education Keywords", len(set(education)))
    col3.metric("Project Keywords", len(set(projects)))

    st.subheader("Search inside document")
    query = st.text_input("Type a keyword")

    if query:
        matches = [line for line in text.split("\n") if query.lower() in line.lower()]
        if matches:
            for m in matches[:10]:
                st.write("•", m)
        else:
            st.info("No matches found")
