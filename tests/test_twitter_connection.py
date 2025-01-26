import unittest
import os
from dotenv import load_dotenv
import tweepy

class TestTwitterConnection(unittest.TestCase):
    def setUp(self):
        # Load environment variables
        load_dotenv()
        
        # Get credentials from environment variables
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    def test_twitter_credentials(self):
        """Test that all required credentials are present"""
        self.assertIsNotNone(self.api_key, "TWITTER_API_KEY is missing")
        self.assertIsNotNone(self.api_secret, "TWITTER_API_SECRET is missing")
        self.assertIsNotNone(self.access_token, "TWITTER_ACCESS_TOKEN is missing")
        self.assertIsNotNone(self.access_token_secret, "TWITTER_ACCESS_TOKEN_SECRET is missing")

    def test_twitter_connection(self):
        """Test Twitter API connection"""
        try:
            # Create OAuth 1.0a authentication
            auth = tweepy.OAuth1UserHandler(
                self.api_key, 
                self.api_secret,
                self.access_token,
                self.access_token_secret
            )
            
            # Create API object
            api = tweepy.API(auth)
            
            # Verify credentials
            user = api.verify_credentials()
            self.assertIsNotNone(user)
            self.assertIsNotNone(user.screen_name)
            print(f"\nSuccessfully authenticated as: @{user.screen_name}")
            
        except tweepy.TweepyException as e:
            self.fail(f"Twitter connection failed: {str(e)}")

if __name__ == '__main__':
    unittest.main() 