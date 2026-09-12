import streamlit as st
import requests

st.set_page_config(page_title="Financial AI Agent", page_icon="📈")
st.title("📈 Multi-Agent Financial Researcher")

st.markdown("### 1. Upload SEC Filing (PDF/HTML)")
uploaded_file = st.file_uploader("Upload a 10-K to vector database", type=["pdf", "htm", "html"])

if st.button("Vectorize Document"):
    if uploaded_file is not None:
        with st.spinner("Chunking and generating HuggingFace embeddings..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            # Call the FastAPI upload endpoint
            response = requests.post("http://api:8000/upload", files=files)
            
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(f"Failed to ingest: {response.text}")
    else:
        st.warning("Please upload a file first.")

st.markdown("---")
st.markdown("### 2. Research Query")
query = st.text_area("Ask the LangGraph Agent a question:")

if st.button("Run Analysis"):
    if query:
        with st.spinner("Planner is decomposing query. Agents are searching PGVector and Tavily..."):
            response = requests.post("http://api:8000/research", json={"query": query})
            
            if response.status_code == 200:
                data = response.json()
                st.markdown("### Final Intelligence Report")
                st.write(data["report"])
                st.caption(f"Sources utilized: {data['sources_checked']['db_chunks']} DB Chunks | {data['sources_checked']['web_articles']} Web Articles")
            else:
                st.error("Analysis failed.")