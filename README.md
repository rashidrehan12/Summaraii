# 🥷 Summaraiii - AI Content Summarization Tool 🗡️

*Summaraiii* is an intelligent AI-powered content summarization web application that helps content creators, researchers, and students extract essential information from multiple sources while filtering out irrelevant content.

<p align="center">
  <pre align="center">
  ╔═══════════════════════════════════════════════════════════╗
  ║                     SUMMARAIII 🗡️                         ║
  ║             Cut the Clutter, Keep the Core                ║
  ╚═══════════════════════════════════════════════════════════╝
  </pre>
</p>

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![Groq](https://img.shields.io/badge/Groq-API-00FF00)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Live Demo

[![Try Summaraii Now](https://img.shields.io/badge/TRY_SUMMARAII-Live_Demo-B22222?style=for-the-badge&logo=streamlit)](https://summaraiii.streamlit.app/)

### ⚔️ Access Summaraii at: [Summaraii.app](https://summaraiii.streamlit.app/)

> 💡 *Note: The demo requires a valid Groq API key for full functionality*

---

## ✨ Features

### 🔥 Core Capabilities

-   **Multi-Source Processing**: YouTube videos, websites, and PDF documents
-   **Topic-Focused Summaries**: AI-powered content filtering based on user-specified topics
-   **Smart Fallback System**: Uses video metadata when transcripts are unavailable
-   **Batch Processing**: Handle multiple URLs and files simultaneously

### 🎯 Input Sources

-   **YouTube Videos**: Automatic transcript extraction and processing
-   **Web Content**: Intelligent web scraping with BeautifulSoup
-   **PDF Documents**: Text extraction and analysis from uploaded files

### 💾 Output & Export

-   **Dual Format Download**: Export as TXT or Markdown files
-   **Comprehensive Reports**: Includes timestamps, sources, and formatted content
-   **Professional Formatting**: Ready-to-use summary documents

### ⚡ Performance

-   **Fast Processing**: Leverages Groq's high-speed LLM inference
-   **Error Resilient**: Robust error handling and fallback mechanisms
-   **Rate Limit Aware**: Smart chunking and API usage optimization

---

## 🚀 Quick Start

### Prerequisites

-   Python 3.8 or higher
-   Groq API account ([Sign up here](https://console.groq.com))
-   Modern web browser

### Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/rashidrehan12/Summaraii.git](https://github.com/rashidrehan12/Summaraii.git)
    cd summaraii
    ```

2.  **Create virtual environment (recommended)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**
    ```bash
    streamlit run cs.py
    ```

5.  **Open your browser** and navigate to `http://localhost:8501`

### Required Dependencies

```txt
streamlit
langchain
langchain-community
langchain-groq
youtube-transcript-api
pytube
beautifulsoup4
requests
validators
pypdf
python-dotenv
````

-----

## 📖 Usage

### Step 1: Configure API

1.  Obtain your Groq API key from [console.groq.com](https://console.groq.com)
2.  Enter the API key in the sidebar (masked for security)
3.  Save your configuration

### Step 2: Set Your Topic

  - Enter a specific topic or subject area
  - Examples: "Machine Learning Algorithms", "Python Web Development", "Data Science Basics"
  - The AI will filter content based on this topic

### Step 3: Add Content Sources

#### 📺 YouTube Videos

```text
[https://www.youtube.com/watch?v=example1](https://www.youtube.com/watch?v=example1)
[https://youtu.be/example2](https://youtu.be/example2)
[https://www.youtube.com/embed/example3](https://www.youtube.com/embed/example3)
```

#### 🌐 Websites

```text
[https://example.com/tutorial](https://example.com/tutorial)
[https://blog.example.com/article](https://blog.example.com/article)
[https://docs.example.com/guide](https://docs.example.com/guide)
```

#### 📃 PDF Documents

  - Drag and drop or select PDF files
  - Supports multiple simultaneous uploads
  - Processes text content efficiently

### Step 4: Generate Summary

  - Click the "Summarize Content" button
  - Monitor real-time processing status
  - View detailed progress for each source

### Step 5: Export Results

  - Download as TXT (plain text) or MD (Markdown)
  - Files include comprehensive metadata
  - Professional formatting for easy sharing

-----

## 🏗️ Architecture

```
Summaraii/
├── cs.py               # Main application file
├── requirements.txt      # Python dependencies
├── README.md           # This file
└── assets/               # Static assets (optional)
    └── icon.png        # Application icon
```

### Key Components

  - **Streamlit Frontend**: Modern web interface
  - **Groq LLM Backend**: High-speed AI processing
  - **Content Processors**: Specialized handlers for each source type
  - **Error Management**: Comprehensive exception handling

-----

## 🔧 Configuration

### Environment Variables (Optional)

```bash
export GROQ_API_KEY=your_api_key_here  # Linux/Mac
set GROQ_API_KEY=your_api_key_here     # Windows
```

### API Rate Limits

  - Default model: `llama-3.1-8b-instant`
  - Automatic chunking for large documents
  - Built-in rate limiting and retry logic

-----

## 🎨 UI Features

  - **Samurai Theme**: Red and gold color scheme
  - **Responsive Design**: Mobile-friendly interface
  - **Real-time Feedback**: Progress indicators and status updates
  - **Intuitive Layout**: Clean, organized sections for each content type

-----

## 💡 Best Practices

### For Optimal Results

1.  **Be Specific**: Use detailed topics for better filtering
2.  **Quality Sources**: Choose content-rich, relevant materials
3.  **Reasonable Volume**: Process 3-5 sources per session
4.  **Verify URLs**: Ensure links are accessible and public

### Performance Tips

  - Use specific keywords in your topic
  - Combine different source types for comprehensive coverage
  - Check video availability before processing
  - For large documents, consider splitting content

-----

## 🐛 Troubleshooting

### Common Issues

**API Errors**

  - Verify Groq API key is valid and active
  - Check account quota and billing status

**YouTube Issues**

  - Some videos may not have available transcripts
  - Application will use metadata as fallback

**Content Access**

  - Ensure URLs are publicly accessible
  - Verify network connectivity

**Installation Problems**

```bash
# If you encounter dependency issues:
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Getting Help

1.  Check the error messages in the application
2.  Verify all dependencies are properly installed
3.  Ensure Python version is 3.8 or higher
4.  Check network connectivity and API key validity

-----

## 📊 Performance

  - Processing speed: 2-5 seconds per source
  - Maximum content size: \~50 pages PDF / 4-hour videos
  - API efficiency: Optimized token usage
  - Memory usage: Efficient chunk processing

-----

## 🔒 Security & Privacy

  - **Local Processing**: All analysis happens in your session
  - **No Data Storage**: Content is not stored on external servers
  - **API Security**: Keys are masked and handled securely
  - **Temporary Files**: Automatic cleanup of processing files

-----

## 🌟 Future Roadmap

  - [ ] Advanced content filtering options
  - [ ] Custom summary templates
  - [ ] Team collaboration features
  - [ ] API usage analytics dashboard
  - [ ] Additional export formats (PDF, Word)
  - [ ] Browser extension integration
  - [ ] Mobile application version

-----

## 🤝 Contributing

We welcome contributions\! Please feel free to:

1.  Fork the repository
2.  Create a feature branch (`git checkout -b feature/amazing-feature`)
3.  Commit your changes (`git commit -m 'Add amazing feature'`)
4.  Push to the branch (`git push origin feature/amazing-feature`)
5.  Open a Pull Request

### Development Setup

```bash
# Clone and setup
git clone [https://github.com/rashidrehan12/Summaraii.git](https://github.com/rashidrehan12/Summaraii.git)
cd summaraii
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run in development mode
streamlit run cs.py
```

-----

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

-----

## 🙏 Acknowledgments

  - Built with [Streamlit](https://streamlit.io/)
  - Powered by [Groq](https://groq.com/) AI inference
  - YouTube processing with [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
  - PDF handling with [PyPDF](https://pypdf.readthedocs.io/)

-----

## 📞 Support

  - **Documentation**: This README
  - **Issues**: [GitHub Issues](https://github.com/rashidrehan12/summaraii/issues)
  - **Questions**: Open a discussion in GitHub
  - **Email**: rashidrehan122000@gmail.com

-----

<p align="center"\>
 Summaraiii 🗡️ - Cutting through the noise to find what matters 
</p\>

<p align="center"\>
<strong\>⭐ Star this repo if you find it useful! </strong\>
</p\>

