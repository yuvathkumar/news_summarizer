# 📰 News Summarization & Hindi Text-to-Speech Application 🚀  

A web-based application that extracts company-related news, performs sentiment analysis, generates comparative insights, and converts summaries into Hindi speech. The project is built with **Python, BeautifulSoup, Streamlit, FastAPI, and deployed on Hugging Face Spaces**.  

---

## 📌 Project Overview  
This project extracts **at least 10 unique news articles** about a given company and performs:  
✔ **News Scraping & Summarization** – Extracts key details like title, summary, topics.  
✔ **Sentiment Analysis** – Classifies news as **Positive, Negative, or Neutral**.  
✔ **Comparative Analysis** – Displays sentiment distribution & topic comparisons.  
✔ **Text-to-Speech (TTS) Conversion** – Converts sentiment summaries into **Hindi audio**.  
✔ **User-Friendly Web Interface** – Users can enter a **company name** and get results.  
✔ **API-based Backend** – Manages data processing and communication between UI and models.  
✔ **Deployed on Hugging Face Spaces** – No local installation required!  

---

## 🚀 Steps to Implement  

### 1️⃣ News Extraction  
- **Library Used:** `BeautifulSoup`  
- **Process:**  
  - Takes a **company name** as input.  
  - Scrapes **at least 10 news articles** from reliable sources.  
  - Extracts **title, summary, and topics** for each article.  

### 2️⃣ Sentiment Analysis  
- **Library Used:** `TextBlob` / `VADER`  
- **Process:**  
  - Analyzes each news article’s sentiment.  
  - Categorizes articles into **Positive, Negative, or Neutral**.  

### 3️⃣ Comparative Analysis  
- **Purpose:** Identify sentiment distribution & common/unique topics.  
- **Outputs:**  
  - **Sentiment Distribution:** Shows the number of Positive, Negative, and Neutral articles.  
  - **Coverage Differences:** Highlights differences in how the company is reported across articles.  
  - **Topic Overlap:** Identifies common & unique topics among articles.  

### 4️⃣ Hindi Text-to-Speech (TTS)  
- **Library Used:** `gTTS` or `VITS`  
- **Process:**  
  - Converts **sentiment summary** into Hindi speech.  
  - Generates an **audio file** that users can listen to.  

### 5️⃣ User Interface (Streamlit)  
- **Library Used:** `Streamlit`  
- **Features:**  
  - Simple UI where users **input a company name**.  
  - Displays extracted news, sentiment scores, and analysis results.  
  - Allows users to **play Hindi audio** summarizing the sentiment.  

### 6️⃣ API Development  
- **Library Used:** `FastAPI`  
- **Endpoints:**  
  - `/extract-news`: Scrapes and processes news articles.  
  - `/analyze-sentiment`: Performs sentiment analysis.  
  - `/generate-tts`: Converts summary into Hindi speech.  
  - `/get-results`: Fetches final structured report.  

## 🛠️ Tech Stack  

| Component            | Technology Used     |
|----------------------|--------------------|
| **Backend**         | Python, FastAPI    |
| **Web Scraping**    | BeautifulSoup      |
| **Sentiment Analysis** | TextBlob / VADER |
| **Text-to-Speech**  | gTTS / VITS        |
| **Frontend**        | Streamlit          |
| **Deployment**      | Hugging Face Spaces |


---

## 📂 Project Structure  
📂 news-summarization-tts
│── app.py # Streamlit UI
│── api.py # FastAPI backend
│── utils.py # Helper functions (scraping, text processing)
│── requirements.txt # Dependencies
│── README.md # Documentation

---


## 🛠️ How to Run the Project
### 1️⃣ Create a Virtual Environment
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```
### 2️⃣ Install Dependencies
  ```bash
    pip install -r requirements.txt
  ```
### 4️⃣ Run the FastAPI Backend Run the FastAPI Backend 
  ```bash
  uvicorn api:app --reload
  ```
- The API will start at http://127.0.0.1:8000.

### 4️⃣ Run the Streamlit Frontend
   ```bash
    streamlit run app.py
  ```
- Open http://localhost:8501/ in your browser.

---

## 🎯 How It Works
- Enter a Company Name – Type a company name (e.g., "Tesla").
- Fetch News – The app scrapes at least 10 news articles
- Analyze Sentiment – Articles are categorized as Positive, Negative, or Neutral.
- Compare Sentiments – Displays sentiment distribution and common topics.
- Generate Hindi Audio – Click to play Hindi speech summarizing the sentiment.

### 📊 Example JSON Output
  ```bash
  {
    "Company": "Tesla",
    "Articles": [
      {
        "Title": "Tesla's New Model Breaks Sales Records",
        "Summary": "Tesla's latest EV sees record sales in Q3...",
        "Sentiment": "Positive",
        "Topics": ["Electric Vehicles", "Stock Market", "Innovation"]
      },
      {
        "Title": "Regulatory Scrutiny on Tesla's Self-Driving Tech",
        "Summary": "Regulators have raised concerns over Tesla’s self-driving software...",
        "Sentiment": "Negative",
        "Topics": ["Regulations", "Autonomous Vehicles"]
      }
    ],
    "Comparative Sentiment Score": {
      "Sentiment Distribution": {
        "Positive": 1,
        "Negative": 1,
        "Neutral": 0
      },
      "Coverage Differences": [
        {
          "Comparison": "Article 1 highlights Tesla's strong sales, while Article 2 discusses regulatory issues.",
          "Impact": "The first article boosts confidence in Tesla's market growth, while the second raises concerns about future regulatory hurdles."
        }
      ],
      "Topic Overlap": {
        "Common Topics": ["Electric Vehicles"],
        "Unique Topics in Article 1": ["Stock Market", "Innovation"],
        "Unique Topics in Article 2": ["Regulations", "Autonomous Vehicles"]
      }
    },
    "Final Sentiment Analysis": "Tesla’s latest news coverage is mostly positive. Potential stock growth expected.",
    "Audio": "[Play Hindi Speech]"
  }
   ```
---

## 💡 Assumptions & Limitations
- Limited to 10+ news articles per search.
- Web scraping restrictions may prevent accessing some news sources.
-- Hindi TTS model may have minor pronunciation errors.

---
## 📤 Submission
- **GitHub Repository**: [news_summarizer](https://github.com/yuvathkumar/news_summarizer)
- **Hugging Face Spaces**: [Live App](https://huggingface.co/spaces/yuvath/NewsSummarizationTTS-v2)

---

# 🏆 Acknowledgments
## Special thanks to [Akaike Technologies] (https://www.akaike.ai/) for this intern assignment.

---

