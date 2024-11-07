import unittest
from datetime import datetime
from news_api_collector import fetch_news, save_news
from db import get_mongo_collection


class NewsCollectorTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up a shared MongoDB collection for tests."""
        cls.collection = get_mongo_collection()

    def sample_article(self):
        """Genera un articolo di esempio unico."""
        return {
            "title": f"Sample News {datetime.now().timestamp()}",
            "url": f"http://example.com/sample-{datetime.now().timestamp()}",
            "description": "Sample description",
            "content": "This is a sample content.",
        }

    def test_fetch_news(self):
        """Test `fetch_news` retrieves a list of articles."""
        category = "Science"
        articles = fetch_news(category)
        self.assertIsInstance(
            articles, list, "fetch_news should retrieve a list of articles"
        )
        if articles:
            self.assertIn(
                "title", articles[0], "Every article should have a 'title' field"
            )

    def test_save_news_inserts_article(self):
        """Test `save_news` inserts a new article in MongoDB."""
        initial_count = self.collection.count_documents({})
        article = self.sample_article()
        save_news([article], "Science")
        new_count = self.collection.count_documents({})
        self.assertGreaterEqual(
            new_count, initial_count + 1, "save_news should insert a new article"
        )

    def test_save_news_avoids_duplicates(self):
        """Test `save_news` avoids inserting duplicates."""
        # Inserisci l'articolo una volta
        article = self.sample_article()
        save_news([article], "Science")
        initial_count = self.collection.count_documents({})

        # Prova a inserire lo stesso articolo
        save_news([article], "Science")
        new_count = self.collection.count_documents({})

        self.assertEqual(
            new_count, initial_count, "save_news should not insert duplicate articles"
        )

    def test_save_news_reports_duplicates(self):
        """Test `save_news` correctly counts duplicates."""
        article = self.sample_article()

        # Inserisci l'articolo la prima volta
        num_inserted, num_duplicates = save_news([article], "Science")
        self.assertEqual(num_inserted, 1, "Should insert article if unique")
        self.assertEqual(
            num_duplicates, 0, "Should not count any duplicates on first insert"
        )

        # Inserisci di nuovo per testare i duplicati
        num_inserted, num_duplicates = save_news([article], "Science")
        self.assertEqual(
            num_inserted, 0, "No new articles should be inserted if duplicate"
        )
        self.assertEqual(num_duplicates, 1, "Should count one duplicate article")


if __name__ == "__main__":
    unittest.main()
