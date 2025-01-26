import os
from dotenv import load_dotenv
import tweepy

def test_twitter_connection():
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    # Verify all credentials are present
    if not all([api_key, api_secret, access_token, access_token_secret]):
        raise ValueError("Missing required Twitter credentials in environment variables")
    
    try:
        # Create OAuth 1.0a authentication
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        # Create API object
        api = tweepy.API(auth)
        
        # Verify credentials
        user = api.verify_credentials()
        print(f"Successfully authenticated as: @{user.screen_name}")
        return True
        
    except tweepy.TweepError as e:
        print(f"Authentication Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_twitter_connection()
    if success:
        print("\nTwitter API connection successful! ✅")
    else:
        print("\nTwitter API connection failed! ❌") 