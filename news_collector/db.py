import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# load virtual environment variables
load_dotenv()

# config MongoDB uri
MONGO_URI = os.getenv("MONGO_URI")


# Initialize MongoDB
def get_mongo_collection():
    client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
    db = client["kindly_positive_feed"]
    # Usa una collezione separata per i test
    collection_name = (
        "news_test" if os.getenv("TEST_ENV", "false") == "true" else "news"
    )
    return db[collection_name]
