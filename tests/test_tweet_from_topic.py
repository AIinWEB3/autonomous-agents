import unittest
from unittest.mock import patch, MagicMock
from src.agent.agent_tools.tweet_from_topic import generate_tweet_from_topic, post_tweet

class TestTweetFromTopic(unittest.TestCase):

    @patch('src.agent.agent_tools.tweet_from_topic.Model')
    def test_generate_tweet_from_topic(self, MockModel):
        # Mock the model's query method
        mock_model_instance = MockModel.return_value
        mock_model_instance.query.return_value = "This is a test tweet about crypto."

        # Call the function
        topic = "crypto"
        tweet = generate_tweet_from_topic(topic)

        # Assertions
        mock_model_instance.query.assert_called_once_with(f"Write a tweet about {topic}. Keep it under 280 characters.")
        self.assertEqual(tweet, "This is a test tweet about crypto.")

    @patch('src.agent.agent_tools.tweet_from_topic.Twitter')
    def test_post_tweet(self, MockTwitter):
        # Mock the Twitter client's post_tweet method
        mock_twitter_instance = MockTwitter.return_value
        mock_twitter_instance.post_tweet.return_value = (True, "1234567890")

        # Call the function
        tweet = "This is a test tweet about crypto."
        post_tweet(tweet)

        # Assertions
        mock_twitter_instance.post_tweet.assert_called_once_with(tweet)

if __name__ == '__main__':
    unittest.main()