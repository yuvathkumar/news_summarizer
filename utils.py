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
            topics = get_topics(title, summary)
            
            articles.append({
                "Title": title,
                "Summary": summary,
                "Sentiment": sentiment,
                "Topics": topics
            })
        
        if not articles:
            print(f"No articles found for {company_name}")
        
        return articles
    
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_sentiment(title, summary):
    text = title + " " + summary
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    negative_cues = {"recall", "concern", "issue", "attack", "fiasco", "pressure", "backlash", "controversy", "uninstall", "vulnerability", "accidentally"}
    if any(cue in text.lower() for cue in negative_cues):
        return "Negative"
    elif polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

def get_topics(title, summary):
    text = title + " " + summary
    blob = TextBlob(text)
    
    phrases = [phrase.lower().replace("’s", "").replace("’t", "").replace("’", "").strip() for phrase in blob.noun_phrases]
    stop_words = {"microsoft", "company", "news", "report", "latest"}
    raw_topics = [phrase for phrase in phrases if len(phrase.split()) > 1 and not any(sw in phrase for sw in stop_words)]
    
    category_map = {
        "Safety": ["safety", "concern", "hazard", "recall", "issue", "vulnerability", "risk"],
        "Innovation": ["feature", "new", "test", "unveiled", "advanced", "interface", "ui", "menu"],
        "Security": ["security", "camera", "attack", "monitor", "hacking", "protection"],
        "Manufacturing": ["manufacturing", "plant", "assembling", "production"],
        "Leadership": ["ceo", "nadella", "secretary", "leadership", "president", "reshuffle", "employees", "officer", "change", "gates"],
        "Sales": ["sales", "trade-in", "buyers", "stock", "purchases", "store", "position", "investment"],
        "Regulation": ["regulators", "administration", "government", "law"],
        "Technology": ["technology", "app", "ai", "system", "update", "software", "windows", "office", "copilot", "pc", "devices", "edge"],
        "Controversy": ["controversy", "backlash", "pressure", "ethical", "removed"],
        "Events": ["event", "anniversary", "celebration", "invites", "visit"],
        "Collaboration": ["collaboration", "together", "share", "discussion"]
    }
    
    topics = set()
    for phrase in raw_topics:
        for category, keywords in category_map.items():
            if any(kw in phrase for kw in keywords):
                topics.add(category)
    
    if topics:
        return sorted(list(topics))[:3]
    else:
        if raw_topics:
            title_words = set(title.lower().split())
            # Score by title overlap, then length as tiebreaker
            best_topic = max(raw_topics, key=lambda p: (len(set(p.split()) & title_words), len(p)))
            if len(best_topic) > 3:
                return [best_topic.capitalize()]
        return ["Miscellaneous"]

# Test
if __name__ == "__main__":
    company = input("Enter a company name: ")
    test_articles = scrape_articles(company)
    for i, article in enumerate(test_articles, 1):
        print(f"Article {i}:")
        print(f"  Title: {article['Title']}")
        print(f"  Summary: {article['Summary']}")
        print(f"  Sentiment: {article['Sentiment']}")
        print(f"  Topics: {article['Topics']}")
        print()