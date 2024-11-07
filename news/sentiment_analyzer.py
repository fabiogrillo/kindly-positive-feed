import os
from transformers import pipeline
from pymongo import MongoClient
from dotenv import load_dotenv
from db import get_mongo_collection
import torch
from tqdm import tqdm

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
    
    for article in tqdm(articles, desc="Running sentiment analysis  on articles", colour="green"):
        title = article.get("title", "")
        description = article.get("description", "")
        full_text = f"{title}\n{description}"  # concatenate title and description

        # Run sentiment analysis on the full text
        result = sentiment_model(full_text)[0]
        label = result["label"]  # "POSITIVE" or "NEGATIVE"
        score = result["score"]  # Confidence score of the sentiment

        article["positive_score"] = score if label == "POSITIVE" else 1 - score
        article["negative_score"] = 1 - score if label == "POSITIVE" else score

        # Rimuovi il campo `_id` per evitare duplicati
        article.pop("_id", None)

        # Store in the appropriate MongoDB collection
        if label == "POSITIVE":
            positive_collection.insert_one(article)
        else:
            negative_collection.insert_one(article)

        # Remove the article from `news` after processing
        news_collection.delete_one({"_id": article["_id"]})
        
        # Delete all remainings articles
        news_collection.delete_many({})

if __name__ == "__main__":
    classify_and_store_articles()
