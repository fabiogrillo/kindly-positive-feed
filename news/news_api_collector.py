import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from db import get_mongo_collection
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Config API and DB
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

# Retrieve the collection from Mongo
collection = get_mongo_collection()

def load_categories(file_path="news/categories.txt"):
    """Load categories from a text file"""
    with open(file_path, "r") as file:
        categories = [line.strip() for line in file if line.strip()]
    return categories

def fetch_news(category):
    """Fetch news about the specified category"""
    params = {
        'apiKey': NEWS_API_KEY,
        'category': category,
        'language': 'en',
        'pageSize': 100
    }
    
    response = requests.get(NEWS_API_URL, params=params)
    return response.json().get('articles', [])

def save_news(articles, category):
    """Save the news on MongoDB"""
    num_inserted_articles = 0
    num_not_inserted_articles = 0
    
    for article in tqdm(articles, desc="Gathering articles", colour="magenta"):
        article['category'] = category
        article['timestamp'] = datetime.now()
        # Check whether an article has been already uploaded
        if not collection.find_one({'url': article['url']}):
            try:
                collection.insert_one(article)
                num_inserted_articles += 1
            except Exception as e:
                print(f"Error during saving: {e}")
        else:
            num_not_inserted_articles += 1
    print(f"Inserted {num_inserted_articles} articles, {num_not_inserted_articles} already saved for `{category}`!")     
    return num_inserted_articles, num_not_inserted_articles

def collect_and_save_news():
    """Download and Save news for each category"""
    categories = load_categories()
    for category in categories:
        articles = fetch_news(category)
        if articles:
            save_news(articles, category)

if __name__ == "__main__":
    collect_and_save_news()
