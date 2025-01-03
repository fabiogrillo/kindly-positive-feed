import os
from transformers import pipeline
from pymongo import MongoClient
from dotenv import load_dotenv
from db import get_mongo_collection
import torch
from tqdm import tqdm
from datasets import Dataset

# Load environment variables
load_dotenv()

# Initialize MongoDB
news_collection = get_mongo_collection()  # This points to the `news` collection
positive_collection = MongoClient(os.getenv("MONGO_URI"))["kindly_positive_feed"]["positive_news"]
negative_collection = MongoClient(os.getenv("MONGO_URI"))["kindly_positive_feed"]["negative_news"]

# Initialize Hugging Face sentiment analysis model with GPU support if available
device = 0 if torch.cuda.is_available() else -1
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    device=device
)

def classify_and_store_articles():
    """Classify articles from the `news` collection and store them in positive or negative collections."""

    articles = list(news_collection.find())

    print(f"There are {len(articles)} articles to process.")
    print("Start processing...")
    
    # Create a dataset from the articles
    dataset = Dataset.from_dict({'text': [f"{article.get('title', '')}\n{article.get('description', '')}" for article in articles]})
    
    results = sentiment_model(dataset["text"], batch_size=8)  # Usa batch_size per migliorare l'efficienza
    
    for article, result in tqdm(zip(articles, results), colour="green", desc="Analyzing sentiments"):
        sentiment = result['label']
        score = result['score']
        
        # Add the sentiment scores to the article
        article["positive_score"] = score if sentiment == "POSITIVE" else 1 - score
        article["negative_score"] = 1 - score if sentiment == "POSITIVE" else score
        
        # Remove 'id' field to avoid duplicates
        article.pop("_id", None)
        
        # Add to the corresponding collection
        if sentiment == 'POSITIVE':
            positive_collection.insert_one(article)
        else:
            negative_collection.insert_one(article)
        
        # Remove the article from the `news` collection after processing
        news_collection.delete_one({"_id": article["_id"]})
    
    # Delete all remaining articles
    news_collection.delete_many({})

    print("Processing completed.")
    
if __name__ == "__main__":
    classify_and_store_articles()
