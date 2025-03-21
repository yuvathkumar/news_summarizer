# api.py
from fastapi import FastAPI
from utils import scrape_articles, comparative_analysis
import os

app = FastAPI()

@app.get("/analyze/{company_name}")
async def analyze_company(company_name: str):
    articles = scrape_articles(company_name)
    print(f"API: Returning {len(articles)} articles for {company_name}")  # Debug print
    result = comparative_analysis(company_name, articles)
    return result

# Run with: uvicorn api:app --reload