# kindly-positive-feed
Kindly is a open source AI-based feed of positive news from the web

# Project Workflow

## Analysis and Advice for the Project

### Crawler and News Gathering
- **Tools**: For simplicity, use News API and The Guardian API to retrieve articles of the selected categories. Use `requests` and `pymongo` modules.
  - [x] **News API**: retrieve articles from it and push them on MongoDB 'News' collection.
  - [ ] **The Guardian API**: retrieve articles from it and push them on MongoDB 'News' collection.
- **Modularization**
  - [x] `news_api_collector.py` for News API integration.
  - [ ] `guardian_api_collector.py` for The Guardian API integration.
  - [x] `db.py` to handle MongoDB initialization, avoiding code duplication.
- **Unit Tests**:
  - [x] Create `test.py` for testing the collectors.
  - [x] Test `fetch_news` function to ensure it retrieves articles correctly.
  - [x] Test `save_news` function to ensure it only saves unique articles to MongoDB
  
---

### Pre-Processing Pipeline
  - [ ] **Sentiment Analysis**: For positive news filtering, use transformers models with Hugging Face. To save memory, start with a pre-trained sentiment model such as VADER or smaller models from DistilBERT, which balance precision and lightness.
  - [ ] **Classification by Scope**: Use topic modeling (e.g., Latent Dirichlet Allocation) or a bag-of-words classification model, easily configured for categories like sports, health, etc.

---

### Database and Storage
- **MongoDB for News**: MongoDB is lightweight, flexible, and handles JSON documents well, perfect for storing unstructured news.
- **PostgreSQL for Users**: Great for storing and managing user data, including interests, feedback, and profiles. PostgreSQL easily supports structured and relational data.
- **Space Limits**: Periodically clean out the database of older news items while maintaining a limited history.

---

### Profiling and Recommendation Algorithm
- [ ] **Collaborative Filtering**: Use lightweight implementations such as Scikit-learn to start. Collect enough user data to achieve good collaborative recommendations.
- [ ] **Feed Customization**: Create an API endpoint where the backend calculates the feed at the time of the request. This enables real-time feed adaptation and transparent model improvements.

---

### Web Extension Frontend
- **React + Tailwind CSS**: Modern and widely used combination for performant, lightweight interfaces. React allows easy modularization of components, like forms and feeds.
- [ ] **Preferences and Interests Collection Form**: Ensure this component is intuitive, so users complete it easily.
- [ ] **Notifications**: Implement a push notification system, e.g., Firebase Cloud Messaging (free up to certain limits).

---

### Extra Features and Optimizations
- [ ] **User Feedback and Machine Learning Explainability**: Use SHAP (SHapley Additive exPlanations) to provide users with insights into why a particular news article was chosen.
- [ ] **NLG for Summaries**: Hugging Face offers models for summarization; a lightweight model like GPT-2 could be suitable.
- [ ] **Social Sharing**: Add a simple button for sharing news on social media directly from the extension.
- [ ] **Mobile Extension**: With React, you could create a mobile app using React Native, allowing reuse of some components.

---

### Running Tests
To run the unit tests for the news collectors:
- set TEST_ENV = true
- run the following command on terminal:
  ```bash
  cd news_collector/
  python -m unittest test.py
  ```