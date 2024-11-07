#!/bin/bash

# Esegui news collector
echo "Collecting news articles..."
python3 news_api_collector.py

# Esegui sentiment analyzer
echo "Classifying and storing articles..."
python3 sentiment_analyzer.py

echo "Pipeline completed!"
