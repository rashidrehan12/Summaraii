import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from bs4 import BeautifulSoup
from langchain_core.documents import Document
import validators
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
from youtube_transcript_api import YouTubeTranscriptApi
import tempfile
import os
import time
from datetime import datetime

# Streamlit Config
st.set_page_config(page_title="Summaraiii 🗡️", page_icon="⚔️", layout="wide")

st.markdown("<h1 style='text-align:center;color:maroon;'>Summaraiii 🗡️</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;color:gold;'>Cut the Clutter, Keep the Core</h4>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    groq_api_key = st.text_input("Groq API Key", type="password", placeholder="Enter Groq API Key")
    search_query = st.text_input("Topic / Title", placeholder="e.g. Artificial Intelligence")

    st.info("Summaraiii delivers concise summaries of content related to your topic 🧠")

# Prompt templates
youtube_metadata_prompt_template = """
Based on the YouTube video metadata and topic "{topic}", summarize what this video likely contains about the topic.

Title: {title}
Channel: {author}
URL: {url}
"""

general_prompt_template = """
Summarize the following content focusing on the topic "{topic}":
{text}
"""

youtube_metadata_prompt = PromptTemplate(template=youtube_metadata_prompt_template, input_variables=["topic", "title", "author", "url"])
general_prompt = PromptTemplate(template=general_prompt_template, input_variables=["text", "topic"])

# Input layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📺 YouTube URLs")
    video_urls = st.text_area("Enter YouTube URLs (one per line)", height=70)

    st.subheader("🌐 Website URLs")
    website_urls = st.text_area("Enter Website URLs (one per line)", height=70)

    st.subheader("📄 Upload PDFs")
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

with col2:
    st.markdown("### ⚔️ Instructions")
    st.markdown("""
    1. Enter your topic  
    2. Add YouTube / Website URLs or upload PDFs  
    3. Click **Summarize Content**  
    """)

# Helper functions
def fetch_website_content(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        content = " ".join(p.get_text().strip() for p in soup.find_all("p"))
        return content[:10000] if content else None
    except Exception as e:
        st.warning(f"Error fetching {url}: {e}")
        return None

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def get_youtube_metadata(video_id):
    try:
        resp = requests.get(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json")
        if resp.status_code == 200:
            data = resp.json()
            return {"title": data["title"], "author": data["author_name"]}
    except:
        return None

def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join(entry["text"] for entry in transcript)
    except:
        return None

def summarize_text(llm, text, topic):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = splitter.split_text(text)
    summaries = []
    for chunk in chunks:
        prompt = general_prompt.format(text=chunk, topic=topic)
        res = llm.invoke(prompt)
        summary = getattr(res, "content", getattr(res, "text", ""))
        if summary:
            summaries.append(summary)
        time.sleep(0.2)
    return " ".join(summaries)

# Button
if st.button("⚔️ Summarize Content"):
    if not groq_api_key:
        st.error("Please enter your Groq API key.")
        st.stop()
    if not search_query:
        st.error("Please enter a topic.")
        st.stop()

    llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)
    combined_summaries = []
    processed_sources = []

    # YouTube
    if video_urls.strip():
        urls = [u.strip() for u in video_urls.splitlines() if u.strip()]
        for url in urls:
            vid = extract_video_id(url)
            if not vid:
                st.warning(f"Invalid YouTube URL: {url}")
                continue
            meta = get_youtube_metadata(vid)
            transcript = get_youtube_transcript(vid)

            st.info(f"📺 Processing: {meta['title'] if meta else url}")
            content = transcript or (meta["title"] + " " + meta["author"])
            summary = summarize_text(llm, content, search_query)
            if summary:
                combined_summaries.append(f"**YouTube: {meta['title'] if meta else url}**\n\n{summary}")
                processed_sources.append(f"YouTube - {url}")
                st.success(f"✅ Summarized {meta['title'] if meta else 'video'}")
            else:
                st.warning(f"No summary generated for {url}")

    # Websites
    if website_urls.strip():
        urls = [u.strip() for u in website_urls.splitlines() if validators.url(u)]
        for url in urls:
            st.info(f"🌐 Processing website: {url}")
            content = fetch_website_content(url)
            if content:
                summary = summarize_text(llm, content, search_query)
                if summary:
                    combined_summaries.append(f"**Website: {url}**\n\n{summary}")
                    processed_sources.append(f"Website - {url}")
                    st.success(f"✅ Summarized website")
            else:
                st.warning(f"No content found at {url}")

    # PDFs
    if uploaded_files:
        for file in uploaded_files:
            st.info(f"📄 Processing PDF: {file.name}")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()
            text = " ".join(doc.page_content for doc in docs)
            os.unlink(tmp_path)
            summary = summarize_text(llm, text, search_query)
            if summary:
                combined_summaries.append(f"**PDF: {file.name}**\n\n{summary}")
                processed_sources.append(f"PDF - {file.name}")
                st.success(f"✅ Summarized PDF")

    # Final summary
    if combined_summaries:
        st.markdown("---")
        st.success("✅ Combining all summaries...")
        combined_text = "\n\n".join(combined_summaries)
        final_prompt = f"Combine the following summaries into one concise summary about '{search_query}':\n{combined_text}"
        final = llm.invoke(final_prompt)
        final_text = getattr(final, "content", getattr(final, "text", "")).strip()

        if final_text:
            st.subheader("🥷 Final Summary:")
            st.text_area("Summary", value=final_text, height=300)

            # Download option
            st.download_button(
                "📥 Download Summary",
                data=final_text,
                file_name=f"summaraiii_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        else:
            st.warning("No final summary generated.")
    else:
        st.warning("No content sources found or summarized.")
