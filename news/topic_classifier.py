import os
from tqdm import tqdm
from bertopic import BERTopic
from pymongo import MongoClient
from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

load_dotenv()

# Initialize MongoDB
positive_collection = MongoClient(os.getenv("MONGO_URI"))["kindly_positive_feed"]["positive_news"]
negative_collection = MongoClient(os.getenv("MONGO_URI"))["kindly_positive_feed"]["negative_news"]
categorized_positive_collection = MongoClient(os.getenv("MONGO_URI"))["kindly_positive_feed"]["categorized_positive_news"]
categorized_negative_collection = MongoClient(os.getenv("MONGO_URI"))["kindly_positive_feed"]["categorized_negative_news"]

# Create a counting vector with stop words
vectorizer_model = CountVectorizer(stop_words="english")

# Init BERTopic
topic_model = BERTopic(language="english", vectorizer_model=vectorizer_model, top_n_words=15)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# Clean text from undesired words
def clean_text(text):
    text = re.sub(r"\[\+\d+ chars\]", "", text)
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = text.lower()
    words = [lemmatizer.lemmatize(word) for word in word_tokenize(text) if word not in stop_words]
    return ' '.join(words)
   
def classify_topics_with_bertopic(collection, categorized_collection):
    articles = list(collection.find())
    documents = [clean_text(f"{article.get('title', '')} {article.get('description', '')} {article.get('content', '')}") for article in articles]
    
    topics, probabilities = topic_model.fit_transform(documents)
    print("Probabilities structure example:", probabilities[:5])

    for article, topic_id, prob in tqdm(zip(articles, topics, probabilities), desc="Getting topics", colour="blue"):
        topic_info = topic_model.get_topic(topic_id)
        topic_words = [word for word, _ in topic_info] if topic_info else ["Unknown"]
    
        # Controlla che la probabilità sia significativa
        if prob > 0.1:  # Qui `prob` è un singolo valore
            article["topics"] = topic_words
        else:
            article["topics"] = ["Uncategorized"]

        categorized_collection.insert_one(article)
        collection.delete_one({"_id": article["_id"]})

        
def process_all_articles():
    """Process articles from both collecitons"""
    classify_topics_with_bertopic(positive_collection, categorized_positive_collection)
    classify_topics_with_bertopic(negative_collection, categorized_negative_collection)
    
if __name__ == "__main__":
    process_all_articles()