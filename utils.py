# utils.py
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from textblob import TextBlob
from collections import Counter

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
    stop_words = {"tesla", "company", "news", "report", "latest"}
    raw_topics = [phrase for phrase in phrases if len(phrase.split()) > 1 and not any(sw in phrase for sw in stop_words)]
    
    category_map = {
        "Safety": ["safety", "concern", "hazard", "recall", "issue", "vulnerability", "risk"],
        "Innovation": ["feature", "new", "test", "unveiled", "advanced", "interface", "ui", "menu"],
        "Security": ["security", "camera", "attack", "monitor", "hacking", "protection"],
        "Manufacturing": ["manufacturing", "plant", "assembling", "production"],
        "Leadership": ["ceo", "musk", "secretary", "leadership", "president", "reshuffle", "employees", "officer", "change"],
        "Sales": ["sales", "trade-in", "buyers", "stock", "purchases", "store", "position", "investment"],
        "Regulation": ["regulators", "administration", "government", "law"],
        "Technology": ["technology", "app", "ai", "system", "update", "software", "windows", "office", "copilot", "pc", "devices", "edge"],
        "Controversy": ["controversy", "backlash", "pressure", "ethical", "removed", "publicity", "reputation"],
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
            # Filter out names (basic heuristic: skip if all lowercase and no keywords)
            filtered_topics = [p for p in raw_topics if not (len(p.split()) == 2 and p.split()[1] in {"musk", "gerber", "nadella"})]
            if filtered_topics:
                best_topic = max(filtered_topics, key=lambda p: (len(set(p.split()) & title_words), len(p)))
                if len(best_topic) > 3:
                    return [best_topic.capitalize()]
        return ["Miscellaneous"]

def comparative_analysis(company_name, articles):
    if not articles:
        return {"Company": company_name, "Articles": [], "Comparative Sentiment Score": {}, "Final Sentiment Analysis": "No data available"}

    sentiments = Counter(article["Sentiment"] for article in articles)
    total = len(articles)
    sentiment_dist = {k: v for k, v in sentiments.items()}

    all_topics = [t for article in articles for t in article["Topics"]]
    topic_counts = Counter(all_topics)
    common_topics = [t for t, c in topic_counts.items() if c > 1]
    unique_topics = {i: [t for t in article["Topics"] if t not in common_topics] 
                     for i, article in enumerate(articles, 1)}

    coverage_diffs = []
    for i in range(len(articles)):
        for j in range(i + 1, len(articles)):
            art1, art2 = articles[i], articles[j]
            diff = {
                "Comparison": f"Article {i+1} ({art1['Sentiment']}) focuses on {', '.join(art1['Topics'])}, "
                            f"while Article {j+1} ({art2['Sentiment']}) covers {', '.join(art2['Topics'])}.",
                "Impact": f"Article {i+1} leans {art1['Sentiment'].lower()} due to {art1['Topics'][0]}, "
                         f"while Article {j+1} leans {art2['Sentiment'].lower()} due to {art2['Topics'][0]}."
            }
            coverage_diffs.append(diff)
            if len(coverage_diffs) >= 2:
                break
        if len(coverage_diffs) >= 2:
            break

    pos, neg = sentiments.get("Positive", 0), sentiments.get("Negative", 0)
    final_summary = "Mixed sentiment with no clear trend."
    if pos > neg + 2:
        final_summary = f"Mostly positive coverage for {company_name}."
    elif neg > pos + 2:
        final_summary = f"Mostly negative coverage for {company_name}."

    return {
        "Company": company_name,
        "Articles": articles,
        "Comparative Sentiment Score": {
            "Sentiment Distribution": sentiment_dist,
            "Coverage Differences": coverage_diffs,
            "Topic Overlap": {
                "Common Topics": common_topics,
                "Unique Topics": {f"Article {i}": ts for i, ts in unique_topics.items() if ts}
            }
        },
        "Final Sentiment Analysis": final_summary,
        "Audio": "[Placeholder for Hindi Speech]"
    }

# Test
if __name__ == "__main__":
    company = input("Enter a company name: ")
    articles = scrape_articles(company)
    result = comparative_analysis(company, articles)
    
    for i, article in enumerate(result["Articles"], 1):
        print(f"Article {i}:")
        print(f"  Title: {article['Title']}")
        print(f"  Summary: {article['Summary']}")
        print(f"  Sentiment: {article['Sentiment']}")
        print(f"  Topics: {article['Topics']}")
        print()
    
    print("Comparative Analysis:")
    print(f"Sentiment Distribution: {result['Comparative Sentiment Score']['Sentiment Distribution']}")
    print("Coverage Differences:")
    for diff in result["Comparative Sentiment Score"]["Coverage Differences"]:
        print(f"  - {diff['Comparison']} {diff['Impact']}")
    print(f"Topic Overlap: {result['Comparative Sentiment Score']['Topic Overlap']}")
    print(f"Final Sentiment: {result['Final Sentiment Analysis']}")