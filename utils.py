# utils.py
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from textblob import TextBlob

def scrape_articles(company_name):
    url = f"https://www.bing.com/news/search?q={company_name}+latest+news&format=rss"
    articles = []
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')[:10]
        
        for item in items:
            title = item.find('title').text.strip() if item.find('title') else "No title"
            desc = item.find('description')
            summary = desc.text.strip() if desc else "No summary available"
            
            soup_desc = BeautifulSoup(summary, 'html.parser')
            summary = soup_desc.get_text(strip=True)[:200]
            
            sentiment = get_sentiment(title, summary)
            
            articles.append({
                "Title": title,
                "Summary": summary,
                "Sentiment": sentiment,
                "Topics": []
            })
        
        if not articles:
            print(f"No articles found for {company_name}")
        
        return articles
    
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_sentiment(title, summary):
    # Combine title and summary for context
    text = title + " " + summary
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    # Adjust thresholds for news context
    if polarity > 0.1:  # Slightly positive threshold
        return "Positive"
    elif polarity < -0.1:  # Slightly negative threshold
        return "Negative"
    else:
        return "Neutral"

# Test
if __name__ == "__main__":
    company = input("Enter a company name: ")
    test_articles = scrape_articles(company)
    for i, article in enumerate(test_articles, 1):
        print(f"Article {i}:")
        print(f"  Title: {article['Title']}")
        print(f"  Summary: {article['Summary']}")
        print(f"  Sentiment: {article['Sentiment']}")
        print()