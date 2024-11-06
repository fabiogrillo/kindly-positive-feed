# kindly-positive-feed
Kindly is a open source AI-based feed of positive news from the web

# Project Workflow

## Analysis and Advice for the Project

### Crawler and News Gathering
- **Tools**: Good choice using Scrapy and BeautifulSoup, which are powerful for scraping and free. Alternating with free news APIs (e.g., NewsAPI and Guardian API) will enrich content.

- **Pre-Processing Pipeline**:
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