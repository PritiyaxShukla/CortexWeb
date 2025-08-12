# 🌐 Cortex Web – AI-Powered Chrome Extension

![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-orange)
![AI](https://img.shields.io/badge/AI-Powered-red)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

**Cortex Web** is an AI-powered Chrome Extension with a Python backend that intelligently processes and summarizes webpage content. It uses advanced NLP models to fetch, analyze, and deliver relevant answers or summaries directly inside your browser.

---

## 🎥 Demo Video
[![Watch Demo](https://img.shields.io/badge/Watch%20Demo-YouTube-red)](https://youtu.be/2uUsNm0JS6o)

---

## 🚀 Features

- **Webpage Text Extraction** – Automatically scrape and fetch webpage content
- **AI Summarization** – Generate concise summaries for long articles or documents
- **Question Answering** – Ask questions based on the current webpage content
- **Custom Chrome Extension Panel** – Easy-to-use popup interface
- **Local Backend Integration** – Python Flask/FastAPI backend for processing

---

## 📂 Project Structure

```
CHROME_EXTENSION/
│
├── .venv/                      # Python virtual environment
│
├── ai_backend/                 # Python backend
│   ├── __pycache__/
│   ├── .env                    # Environment variables
│   ├── app.py                  # Backend server
│   ├── demo.py
│   ├── fetched_text.txt        # Raw fetched webpage text
│   ├── practice.py
│   ├── question_answer.py      # Q&A module
│   ├── requirements.txt        # Python dependencies
│   ├── scraped_output.txt      # Processed/scraped data
│   └── summary.py              # Summarization module
│
├── extension/                  # Chrome extension frontend
│   ├── background.js           # Background service worker
│   ├── icon.png
│   ├── icon2.png
│   ├── manifest.json           # Chrome extension manifest
│   ├── popup.js                # Popup UI logic
│   ├── sidepanel.html          # UI HTML file
│   └── style.css               # Stylesheet
│
├── AI_Summary_project_notes.txt # Project notes
├── image (3).png               # Example image/screenshot
└── requirements.txt            # Additional dependencies
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/cortex-web.git
cd cortex-web
```

### 2️⃣ Setup Python Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r ai_backend/requirements.txt
```

### 4️⃣ Configure API Key
Edit `app.py` and add your API key in the designated variable.

### 5️⃣ Start Backend Server
```bash
cd ai_backend
python app.py
```

The server will be running at: **http://127.0.0.1:5000**

---

## 🖥️ Loading Chrome Extension

1. Open **Google Chrome**
2. Navigate to **chrome://extensions/**
3. Enable **Developer Mode** (toggle in top-right corner)
4. Click **"Load unpacked"**
5. Select the **extension/** folder from your project directory
6. The extension will now appear in your Chrome toolbar

---

## 📌 How to Use

1. **Start the Python backend** by running `python app.py`
2. **Load the Chrome extension** following the steps above
3. **Open any webpage** you want to analyze
4. **Click the extension icon** in your Chrome toolbar
5. **Choose your action:**
   - **Summarize** – Get a concise summary of the webpage
   - **Ask a Question** – Query specific information from the page content

---

## 🛠️ Tech Stack

- **Frontend:** Chrome Extension (JavaScript, HTML, CSS)
- **Backend:** Python Flask
- **AI/NLP:** Advanced language models for text processing
- **Web Scraping:** Automated content extraction
- **Storage:** Local text file storage

---

## 📋 Requirements

### Python Dependencies
```txt
flask
requests
beautifulsoup4
transformers
torch
```

### System Requirements
- Python 3.8+
- Google Chrome Browser
- Internet connection for AI model access

---

## 🎥 Demo & Links

- **YouTube Demo:** [Watch Here](https://youtu.be/2uUsNm0JS6o)
- **LinkedIn Profile:** [Pritiyax Shukla](https://www.linkedin.com/in/pritiyax-shukla-0646982b3/)

---

## 🚀 Future Enhancements

- [ ] Support for multiple AI models
- [ ] Batch processing for multiple tabs
- [ ] Export summaries to different formats
- [ ] User preference settings
- [ ] Dark/Light theme toggle
- [ ] Integration with popular note-taking apps

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact

**Pritiyax Shukla**
- LinkedIn: [Pritiyax Shukla](https://www.linkedin.com/in/pritiyax-shukla-0646982b3/)
- YouTube: [Watch Demo](https://youtu.be/2uUsNm0JS6o)

---

## 🙏 Acknowledgments

- Built with modern web technologies and AI frameworks
- Inspired by the need for efficient web content processing
- Thanks to the open-source community for various tools and libraries used

---

⭐ **If you found this project helpful, please give it a star!**