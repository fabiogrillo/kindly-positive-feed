#!/bin/bash

# Attiva l'ambiente virtuale
source venv/bin/activate

# Esegui news collector
echo "Collecting news articles..."
python3 news_api_collector.py

# Esegui sentiment analyzer
echo "Classifying and storing articles..."
python3 sentiment_analyzer.py

# Classify topics
echo "Classifying topics"
python3 topic_classifier.py

echo "Pipeline completed!"
