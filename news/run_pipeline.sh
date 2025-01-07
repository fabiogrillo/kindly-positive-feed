#!/bin/bash

# Esegui news collector
echo "Collecting news articles..."
python3 news/news_api_collector.py

# Esegui sentiment analyzer
echo "Classifying and storing articles..."
python3 news/sentiment_analyzer.py

# Classify topics
echo "Classifying topics"
python3 news/topic_classifier.py

echo "Pipeline completed!"
