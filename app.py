# app.py
import streamlit as st
import requests
import os
import plotly.express as px
import pandas as pd

# Custom CSS for clean, meaningful styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 30px;
        font-family: 'Poppins', sans-serif;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #ffca28;
        color: #1e3c72;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
    }
    .article-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .article-card:hover {
        transform: translateY(-8px);
    }
    .section-title {
        color: #ffca28;
        font-size: 32px;
        font-weight: 700;
        margin-top: 40px;
        border-bottom: 3px solid #ffca28;
        padding-bottom: 8px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    .topic-badge {
        background-color: #ffca28;
        color: #1e3c72;
        padding: 6px 12px;
        border-radius: 20px;
        margin-right: 8px;
        font-size: 13px;
        font-weight: 500;
    }
    .audio-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        margin-top: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
        border: 2px solid #ffca28;
        width: 50%;
        margin-left: auto;
        margin-right: auto;
    }
    .audio-title {
        color: #ffca28;
        font-size: 24px;
        font-weight: 600;
        text-align: center;
    }
    .audio-description {
        color: #ffffff;
        font-size: 16px;
        text-align: center;
        margin-bottom: 10px;
    }
    .stAudio {
        width: 100%;
        border-radius: 10px;
    }
    .stDownloadButton>button {
        background-color: #ffca28;
        color: #1e3c72;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
    }
    .sidebar .sidebar-content {
        background-color: #2a5298;
        color: #ffffff;
    }
    .sidebar .stRadio > label {
        color: #ffffff;
        font-weight: 500;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #1e3c72;
        border-radius: 10px;
        border: 2px solid #ffca28;
    }
    .stMultiSelect > div > div {
        background-color: #ffffff;
        border-radius: 10px;
        border: 2px solid #ffca28;
    }
    .topic-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        border-left: 5px solid #ffca28;
        width: 50%;
        margin-left: auto;
        margin-right: auto;
    }
    .topic-header {
        color: #1e3c72;
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 15px;
        border-bottom: 2px solid #ffca28;
        padding-bottom: 5px;
    }
    .topic-item {
        color: #1e3c72;
        font-size: 16px;
        margin: 8px 0;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("Use the options below to explore the app.")
page = st.sidebar.radio("Go to", ["Home", "Analysis", "Audio"])

# Main App
st.title("📰 News Summarization & TTS App")

if page == "Home":
    st.markdown("Enter a company name to fetch the latest news, analyze sentiments, and hear a Hindi audio summary.", unsafe_allow_html=True)
    with st.container():
        # Text input with no placeholder
        company_name = st.text_input("Enter a company name (e.g., Tesla, Microsoft):", value="", key="company_name_input")
        
        if st.button("Analyze"):
            if not company_name:
                st.warning("Please enter a company name.")
            else:
                with st.spinner("Fetching and analyzing news..."):
                    response = requests.get(f"http://localhost:8000/analyze/{company_name}")
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.result = result
                    else:
                        st.error("Error fetching data from API.")

if "result" in st.session_state:
    result = st.session_state.result
    
    if page == "Home":
        # Articles Section (Home Page)
        st.markdown("<div class='section-title'>Articles</div>", unsafe_allow_html=True)
        sentiment_filter = st.multiselect("Filter by Sentiment", ["Positive", "Negative", "Neutral"], default=["Positive", "Negative", "Neutral"])
        
        for i, article in enumerate(result["Articles"], 1):
            if article["Sentiment"] in sentiment_filter:
                with st.expander(f"Article {i}: {article['Title']}"):
                    st.markdown(f"""
                        <div class='article-card'>
                            <b>Summary:</b> {article['Summary']}<br>
                            <b>Sentiment:</b> {article['Sentiment']}<br>
                            <b>Topics:</b> {' '.join([f'<span class="topic-badge">{t}</span>' for t in article['Topics']])}
                        </div>
                    """, unsafe_allow_html=True)
    
    if page == "Analysis":
        # Comparative Analysis Section (No Articles)
        st.markdown("<div class='section-title'>Comparative Analysis</div>", unsafe_allow_html=True)
        
        # Sentiment Distribution Chart
        dist = result["Comparative Sentiment Score"]["Sentiment Distribution"]
        df = pd.DataFrame(list(dist.items()), columns=["Sentiment", "Count"])
        fig = px.pie(df, names="Sentiment", values="Count", title="Sentiment Distribution", 
                     color_discrete_sequence=["#FF4B4B", "#4CAF50", "#FFD700"])
        st.plotly_chart(fig, use_container_width=True)
        
        # Coverage Differences
        st.write("**Coverage Differences:**")
        for diff in result["Comparative Sentiment Score"]["Coverage Differences"]:
            st.write(f"- {diff['Comparison']} {diff['Impact']}")
        
        # Topic Overlap - Enhanced Display
        st.markdown("<div class='section-title'>Topic Overlap</div>", unsafe_allow_html=True)
        overlap = result["Comparative Sentiment Score"]["Topic Overlap"]
        
        # Common Topics Card
        st.markdown("<div class='topic-card'>", unsafe_allow_html=True)
        st.markdown("<div class='topic-header'>Common Topics</div>", unsafe_allow_html=True)
        if overlap["Common Topics"]:
            for topic in overlap["Common Topics"]:
                st.markdown(f"<div class='topic-item'>- {topic}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='topic-item'>No common topics found.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Unique Topics Card
        st.markdown("<div class='topic-card'>", unsafe_allow_html=True)
        st.markdown("<div class='topic-header'>Unique Topics</div>", unsafe_allow_html=True)
        if overlap["Unique Topics"]:
            for article, topics in overlap["Unique Topics"].items():
                st.markdown(f"<div class='topic-item'>{article}: {', '.join(topics)}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='topic-item'>No unique topics found.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Final Sentiment
        st.write(f"**Final Sentiment:** {result['Final Sentiment Analysis']}")
    
    if page == "Audio":
        # Hindi Audio Section
        st.markdown("<div class='audio-container'>", unsafe_allow_html=True)
        st.markdown("<div class='audio-title'>Hindi Audio Summary</div>", unsafe_allow_html=True)
        audio_file = result["Audio"]
        if os.path.exists(audio_file):
            st.markdown("<div class='audio-description'>Listen to the sentiment summary in Hindi:</div>", unsafe_allow_html=True)
            st.audio(audio_file, format="audio/mp3")
            with open(audio_file, "rb") as file:
                st.download_button(
                    label="Download Hindi Audio",
                    data=file,
                    file_name=audio_file,
                    mime="audio/mp3"
                )
        else:
            st.error("Audio file not found.")
        st.markdown("</div>", unsafe_allow_html=True)