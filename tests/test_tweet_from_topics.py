import unittest
from unittest.mock import patch, MagicMock
from src.agent.agent_tools.tweet_from_topics import generate_tweet_from_concept, post_tweet
from src.agent.agent_tools.topics import TOPICS

class TestTweetFromTopics(unittest.TestCase):
    def setUp(self):
        self.mock_model = MagicMock()
        self.mock_model.query.return_value = "This is a test response about crypto concepts."

    def test_generate_tweet_from_concept(self):
        """Test that tweet generation works correctly"""
        concept = "Bitcoin"
        tweet = generate_tweet_from_concept(concept, self.mock_model)
        
        # Check tweet format
        self.assertIn("🔥 Crypto Knowledge Drop: Bitcoin", tweet)
        self.assertIn("#Crypto #Web3 #CryptoEducation", tweet)
        self.assertLess(len(tweet), 280)  # Twitter character limit

    @patch('tweepy.Client')
    def test_post_tweet_success(self, mock_client):
        """Test successful tweet posting"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.data = {'id': '123456'}
        mock_client.return_value.create_tweet.return_value = mock_response
        
        # Test
        tweet = "Test tweet"
        result = post_tweet(tweet)
        
        # Verify
        self.assertTrue(result)
        mock_client.return_value.create_tweet.assert_called_once_with(text=tweet)

    @patch('tweepy.Client')
    def test_post_tweet_failure(self, mock_client):
        """Test tweet posting failure"""
        # Setup mock to raise an exception
        mock_client.return_value.create_tweet.side_effect = Exception("Tweet failed")
        
        # Test
        tweet = "Test tweet"
        result = post_tweet(tweet)
        
        # Verify
        self.assertFalse(result)

    def test_topics_not_empty(self):
        """Test that we have topics to tweet about"""
        self.assertGreater(len(TOPICS), 0)
        
    def test_topics_format(self):
        """Test that topics are properly formatted strings"""
        for topic in TOPICS.values():
            self.assertIsInstance(topic, str)
            self.assertGreater(len(topic), 0)

if __name__ == '__main__':
    unittest.main() 