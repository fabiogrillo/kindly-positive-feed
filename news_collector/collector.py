import os
import requests
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from dotenv import load_dotenv

# load virtual environment variables
load_dotenv()

# config api and db
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
MONGO_URI = os.getenv('MONGO_URI')

# Initialize MongoDB
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client['kindly_positive_feed']
collection = db['news']

def fetch_news(category):
    """Fetch news about the specified category"""
    params = {
        'apiKey': NEWS_API_KEY,
        'category': category,
        'language': 'en',
        'pageSize': 100
    }
    
    response = requests.get(NEWS_API_URL, params=params)
    # print(response.json().get('articles', []))
    return response.json().get('articles', [])

def save_news(articles, category):
    """Save the news on MongoDB"""
    num_inserted_articles = 0
    num_not_inserted_articles = 0
    
    for article in articles:
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
                     
def collect_and_save_news(categories):
    """Download and Save news for each category"""
    for category in categories:
        articles = fetch_news(category)
        if articles:
            save_news(articles, category)
        
if __name__ == "__main__":
    
    categories = ['Science', 'Sports'] # TODO: add new categories!
    
    collect_and_save_news(categories)