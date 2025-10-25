import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from bs4 import BeautifulSoup
from langchain.schema import Document
import validators
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
from youtube_transcript_api import YouTubeTranscriptApi
import tempfile
import os
import time
import json
from datetime import datetime

# SVG code
svg_code = '''
<svg fill="#000000" height="100px" width="100px" version="1.1" id="_x31_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 303 256" xml:space="preserve">
  <defs>
    <linearGradient id="maroonGoldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color: maroon; stop-opacity: 1" />
      <stop offset="100%" style="stop-color: gold; stop-opacity: 1" />
    </linearGradient>
  </defs>
  <g id="SVGRepo_bgCarrier" stroke-width="0" />
  <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" />
  <g id="SVGRepo_iconCarrier">
    <path id="_x33_" fill="url(#maroonGoldGradient)" d="M295.3,130.2c-15.4-4.8-17.2-13.5-22.7-18.8c-11.7-11.7-27.1-1.4-33.2,3.4c-6.6-37.4-33.5-65.1-83.2-65.1 
    c-58.2,0-85.3,38.1-85.3,85.3s28,111.9,85.3,111.9s85.3-64.6,85.3-111.9c0-0.5,0-1.1,0-1.6c10.5,3,11.2,14.9,11.2,14.9 
    s0,24.1,21.3,24.1c-7.8-14.4-2.8-21.8-2.8-29.3c0-4.8-1.6-8.3-3.7-11.2C272.8,135.7,284.7,141.2,295.3,130.2z M221.2,145.5 
    c0,11.7-9.6,21.5-21.3,24.1c-5,1.1-24.5,2.8-44,2.8l0,0l0,0c-19.5,0-39-1.6-44-2.8c-11.7-2.3-21.3-12.2-21.3-24.1v-6 
    c0-6,5-10.5,10.5-10.5c18.6,0,25.4,5.3,54.6,5.3s36-5.3,54.6-5.3c5.5,0,10.5,4.8,10.5,10.5v6H221.2z" />
    <path id="_x32__1_" fill="url(#maroonGoldGradient)" d="M136.9,157.9c-0.5,0-0.7,0-1.4-0.2l-30.3-11c-2.1-0.7-3.2-3-2.3-5c0.7-2.1,3-3.2,5-2.3l30.3,11 
    c2.1,0.7,3.2,3,2.3,5C140.1,157,138.5,157.9,136.9,157.9z" />
    <path id="_x32_" fill="url(#maroonGoldGradient)" d="M175.1,157.9c-1.6,0-3.2-1.1-3.7-2.8c-0.7-2.1,0.2-4.4,2.3-5l30.3-11c2.1-0.7,4.4,0.2,5,2.3 
    c0.7,2.1-0.2,4.4-2.3,5l-30.3,11C176.3,157.9,175.8,157.9,175.1,157.9z" />
    <path id="_x31__1_" fill="url(#maroonGoldGradient)" d="M90.5,48.6c-2.1-2.1-5.3-2.1-7.6,0l-6.6,6.6L29.6,8c-3-3-7.6-3-10.3,0L11,16.2
    c-3,3-3,7.6,0,10.3l46.8,46.8L51.1,80c-2.1,2.1-2.1,5.3,0,7.6c1.1,1.4,2.3,1.8,3.7,1.8s2.8-0.5,3.7-1.6l6.6-6.6l9.4,9.4 
    c0.7-1.6,1.6-3.4,2.3-5l-8-8L80,66.2l6.2,6.2c1.1-1.4,2.3-2.8,3.7-3.9l-6-6l6.6-6.6C92.6,53.8,92.6,50.6,90.5,48.6z 
    M35.8,33.2H25.2V22.7h10.5V33.2z M49.1,46.5H38.5V36h10.5V46.5z M51.6,59.8V49.3h10.5v10.5H51.6z" />
  </g>
</svg>
'''

# Set up the Streamlit app configuration
st.set_page_config(page_title="Summaraiii 🗡️ : Cut the Clutter, Keep the Core", page_icon="icon.png", layout="wide")

# CSS for Summaraiii styling
st.markdown("""
    <style>
    .main-header {
        color: #B22222;
        text-align: center;
        font-weight: bold;
        font-size: 42px;
    }
    .sub-header {
        text-align: center;
        color: #DAA520;
        font-style: italic;
        margin-bottom: 25px;
        font-size: 18px;
    }
    .stButton>button {
        border-radius: 8px;
        background-color: #B22222;
        color: white;
        font-size: 18px;
        font-weight: bold;
        margin-top: 20px;
    }
    .stTextArea textarea {
        border: 1px solid #FFD700;
        border-radius: 10px;
    }
    .download-btn {
        background-color: #DAA520 !important;
        color: #000 !important;
        border: 2px solid #B22222 !important;
        font-weight: bold;
    }
    .download-btn:hover {
        background-color: #FFD700 !important;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin-bottom: 20px;
    }
    .header-container img {
        height: 100px;
    }
    .main-header {
        font-size: 2.5em;
        color: #B22222;
    }
    .sub-header {
        font-size: 1.5em;
        color: #FFD700;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(f'''
    <div class="header-container">
        <div>{svg_code}</div>
        <div>
            <h1 class="main-header">Summaraiii 🗡️</h1>
            <h3 class="sub-header">Cut the Clutter, Keep the Core</h3>
        </div>
    </div>
''', unsafe_allow_html=True)

# Sidebar for Groq API Key and Search Query
with st.sidebar:
    st.markdown(f'<div style="text-align: center;">{svg_code}</div>', unsafe_allow_html=True)
    st.header("   🗡️ Summaraiii 🗡️ ")
    st.markdown("Summarize reference content for content creators🥷")
    st.subheader("API Configuration")
    groq_api_key = st.text_input("Groq API Key", value="", type="password", placeholder="⚔️Enter Groq API Key here⚔️")
    st.subheader("Topic")
    search_query = st.text_input("Enter the Topic/Title", placeholder="e.g. Python")
    st.subheader("About Summaraiii ✒️")
    st.markdown("**Summaraiii** delivers a concise summary, focusing only on relevant data, just like a samurai cuts down to the essentials.")
    st.subheader("Tips for Best Results:")
    st.markdown("""
                1. Ensure that the URLs and PDFs you provide contain content relevant to the topic you've specified.
                2. If a URL or PDF does not contain relevant content, Summaraiii will notify you.
                3. For optimal summaries, make sure to provide clear and specific topics.
            """)

# Prompt Templates
youtube_metadata_prompt_template = """
Based on the YouTube video metadata and the topic "{topic}", provide an informed summary of what this video likely contains about the topic.

VIDEO INFORMATION:
- Title: {title}
- Channel: {author}
- URL: {url}

TOPIC: {topic}

Please analyze the video title and channel to infer what content this video might contain related to the topic. Provide a summary based on this analysis, focusing specifically on aspects relevant to "{topic}".
"""

general_prompt_template = """
Given the topic "{topic}", summarize the key information relevant to the topic from the following content:
Content: {text}

Provide a concise summary focusing only on information relevant to the topic.
"""

youtube_metadata_prompt = PromptTemplate(template=youtube_metadata_prompt_template, input_variables=["topic", "title", "author", "url"])
general_prompt = PromptTemplate(template=general_prompt_template, input_variables=["text", "topic"])

# Layout for inputs
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📺 YouTube Video URLs")
    video_urls = st.text_area("Enter YouTube Video URLs (one per line)", placeholder="e.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ" ,height=30)

    st.subheader("🌐 Website URLs")
    website_urls = st.text_area("Enter Website URLs (one per line)", placeholder="e.g. https://www.example.com", height=30)

    st.subheader("📃 Upload PDFs")
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

with col2:
    st.markdown("<h3 style='text-align: center;'>⚔️ Instructions ⚔️</h3>", unsafe_allow_html=True)
    st.markdown("""
    1. **Topic:** Provide a topic to filter relevant content.
    2. **YouTube Video URLs:** Enter YouTube URLs (one per line). 
    3. **Website URLs:** Enter website URLs (one per line).
    4. **Upload PDFs:** Upload PDF files.
    5. Click **"Summarize Content"** to begin.
    6. **Download** your summary when complete.
    """)

# Helper functions
def fetch_website_content(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.decompose()
            
        paragraphs = soup.find_all('p')
        content = "\极".join([para.get_text().strip() for para in paragraphs if para.get_text().strip()])
        
        article = soup.find('article')
        if article:
            article_content = article.get_text().strip()
            if len(article_content) > len(content):
                content = article_content
                
        return content if content else None
    except Exception as e:
        st.error(f"Error fetching website content: {e}")
        return None

def extract_video_id(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11})',
        r'youtu\.be\/([0-9A-Za-z_-]{11})',
        r'embed\/([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_youtube_metadata(video_id):
    try:
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(oembed_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'title': data.get('title', 'Unknown Title'),
                'author': data.get('author_name', 'Unknown Channel'),
                'thumbnail_url': data.get('thumbnail_url', '')
            }
    except:
        return None

def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except:
        return None

def filter_content(content, query):
    if query:
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        return "\n".join([line for line in content.split('\n') if pattern.search(line)])
    return content

def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', ' ', text)

def is_relevant(content, topic):
    if not content or not topic:
        return False
    content_lower = content.lower()
    topic_lower = topic.lower()
    keywords = re.findall(r'\b\w{3,}\b', topic_lower)
    return any(keyword in content_lower for keyword in keywords)

def summarize_youtube_metadata(llm, metadata, topic, url):
    """Summarize YouTube video using metadata when transcript is unavailable"""
    try:
        prompt = youtube_metadata_prompt.format(
            topic=topic,
            title=metadata['title'],
            author=metadata['author'],
            url=url
        )
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        st.error(f"Error summarizing YouTube metadata: {e}")
        return None

def summarize_general_content(llm, content, topic):
    """Summarize general content with chunking"""
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200,
            length_function=len
        )
        
        chunks = text_splitter.split_text(content)
        summaries = []
        
        for chunk in chunks:
            if len(chunk) > 100:
                try:
                    chunk_prompt = general_prompt.format(text=chunk, topic=topic)
                    response = llm.invoke(chunk_prompt)
                    summaries.append(response.content)
                    time.sleep(0.3)
                except Exception as e:
                    continue
        
        return " ".join(summaries) if summaries else None
        
    except Exception as e:
        st.error(f"Error summarizing content: {e}")
        return None

def create_download_data(summary, topic, sources):
    """Create formatted data for download"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    download_data = f"""
# Summaraiii Summary Report
## Generated on: {timestamp}
## Topic: {topic}

## 📋 Summary
{summary}

## 📊 Sources Processed
{chr(10).join([f"- {source}" for source in sources])}

---
*Generated by Summaraiii 🗡️ - Cut the Clutter, Keep the Core*
"""
    return download_data

# Button click logic
if st.button("Summarize Content", key="summarize"):
    if not groq_api_key.strip():
        st.error("Please provide the API key.")
        st.stop()
    if not search_query.strip():
        st.error("Please provide topic to search.")
        st.stop()

    try:
        llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key, temperature=0.1)
    except Exception as e:
        st.error(f"Error initializing Groq API: {e}")
        st.stop()

    combined_summaries = []
    processed_sources = []

    # Process YouTube URLs
    if video_urls.strip():
        video_urls_list = [url.strip() for url in video_urls.split("\n") if url.strip()]
        
        for url in video_urls_list:
            try:
                video_id = extract_video_id(url)
                if not video_id:
                    st.warning(f"❌ Invalid YouTube URL: {url}")
                    continue
                
                metadata = get_youtube_metadata(video_id)
                video_title = metadata['title'] if metadata else "Unknown Title"
                
                st.info(f"📺 Processing YouTube: {video_title}")
                
                # Try to get transcript first
                transcript = get_youtube_transcript(video_id)
                
                if transcript:
                    if is_relevant(transcript, search_query):
                        filtered_content = filter_content(transcript, search_query)
                        if filtered_content:
                            summary = summarize_general_content(llm, filtered_content, search_query)
                            if summary:
                                combined_summaries.append(f"**YouTube Transcript: {video_title}**\n\n{summary}")
                                processed_sources.append(f"YouTube: {video_title}")
                                st.success(f"✅ Processed YouTube transcript")
                            else:
                                st.warning(f"❌ Could not summarize YouTube transcript: {video_title}")
                        else:
                            st.warning(f"❌ No relevant content in YouTube video: {video_title}")
                    else:
                        st.warning(f"❌ YouTube video not relevant to topic: {video_title}")
                else:
                    # Fallback to metadata summarization
                    if metadata and is_relevant(metadata['title'], search_query):
                        summary = summarize_youtube_metadata(llm, metadata, search_query, url)
                        if summary:
                            combined_summaries.append(f"**YouTube Metadata: {video_title}**\n\n{summary}")
                            processed_sources.append(f"YouTube (Metadata): {video_title}")
                            st.success(f"✅ Processed YouTube metadata")
                        else:
                            st.warning(f"❌ Could not summarize YouTube metadata: {video_title}")
                    else:
                        st.warning(f"❌ YouTube video not relevant to topic: {video_title}")
                    
            except Exception as e:
                st.error(f"❌ Error processing YouTube URL {url}: {e}")

    # Process Websites
    if website_urls.strip():
        website_urls_list = [url.strip() for url in website_urls.split("\n") if url.strip() and validators.url(url)]
        
        for url in website_urls_list:
            try:
                st.info(f"🌐 Processing website: {url}")
                content = fetch_website_content(url)
                
                if content:
                    if is_relevant(content, search_query):
                        filtered_content = filter_content(content, search_query)
                        if filtered_content:
                            summary = summarize_general_content(llm, filtered_content, search_query)
                            if summary:
                                combined_summaries.append(f"**Website: {url}**\n\n{summary}")
                                processed_sources.append(f"Website: {url}")
                                st.success(f"✅ Processed website")
                            else:
                                st.warning(f"❌ Could not summarize website: {url}")
                        else:
                            st.warning(f"❌ No relevant content on website: {url}")
                    else:
                        st.warning(f"❌ Website content not relevant to topic: {url}")
                else:
                    st.warning(f"❌ Could not fetch content from website: {url}")
                    
            except Exception as e:
                st.error(f"❌ Error processing website {url}: {e}")

    # Process PDFs
    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                st.info(f"📃 Processing PDF: {uploaded_file.name}")
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_file_path = temp_file.name

                loader = PyPDFLoader(temp_file_path)
                docs = loader.load()
                
                pdf_content = ""
                for doc in docs:
                    pdf_content += doc.page_content + "\n"
                
                if is_relevant(pdf_content, search_query):
                    filtered_content = filter_content(pdf_content, search_query)
                    if filtered_content:
                        summary = summarize_general_content(llm, filtered_content, search_query)
                        if summary:
                            combined_summaries.append(f"**PDF: {uploaded_file.name}**\n\n{summary}")
                            processed_sources.append(f"PDF: {uploaded_file.name}")
                            st.success(f"✅ Processed PDF")
                        else:
                            st.warning(f"❌ Could not summarize PDF: {uploaded_file.name}")
                    else:
                        st.warning(f"❌ No relevant content in PDF: {uploaded_file.name}")
                else:
                    st.warning(f"❌ PDF content not relevant to topic: {uploaded_file.name}")
                    
            except Exception as e:
                st.error(f"❌ Error processing PDF {uploaded_file.name}: {e}")
            finally:
                if 'temp_file_path' in locals():
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass

    # Generate final summary
    if combined_summaries:
        try:
            final_content = "\n\n".join(combined_summaries)
            
            # Create a final combined summary
            final_prompt = f"""
            Combine the following summaries into one comprehensive summary about "{search_query}":
            
            {final_content}
            
            Please provide a well-organized final summary that captures all key points.
            """
            
            final_summary = llm.invoke(final_prompt)
            
            st.success("✅ Combined Summary:")
            summary_text = final_summary.content
            st.text_area("🥷 Summary:", value=summary_text, height=300, key="summary_output")
            
            st.info(f"📊 Processed {len(processed_sources)} sources:")
            for source in processed_sources:
                st.write(f"• {source}")
            
            # Download functionality
            st.markdown("---")
            st.subheader("📥 Download Summary")
            
            # Create download data
            download_content = create_download_data(summary_text, search_query, processed_sources)
            
            # Download buttons
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    label="📄 Download as TXT",
                    data=download_content,
                    file_name=f"summaraiii_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    key="download_txt",
                    use_container_width=True,
                    help="Download summary as text file"
                )
            
            with col2:
                st.download_button(
                    label="📝 Download as MD",
                    data=download_content,
                    file_name=f"summaraiii_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    key="download_md",
                    use_container_width=True,
                    help="Download summary as Markdown file"
                )
                
        except Exception as e:
            st.error(f"Error generating final summary: {e}")
    else:
        st.warning("❌ No relevant content found for the specified topic.")

# Add footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>Summaraiii 🗡️ - Cutting through the noise to find what matters</div>", unsafe_allow_html=True)
