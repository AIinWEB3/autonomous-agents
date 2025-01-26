import os
import tweepy
from pprint import pp
import time
from tweepy.errors import TooManyRequests, TwitterServerError
from dotenv import load_dotenv
from src.agent.agent_tools.model import Model

def generate_tweet_from_topic(topic):
    # Load environment variables
    load_dotenv()

    # Initialize the model
    model = Model(
        api_key=os.getenv("MODEL_API_KEY"),
        url=os.getenv("MODEL_URL"),
        model=os.getenv("MODEL_NAME")
    )

    # Construct the prompt for the model
    prompt = f"Write a tweet about {topic}. Keep it under 280 characters."

    # Query the model to generate a tweet
    tweet = model.query(prompt)

    return tweet

def post_tweet(tweet):
    # Load environment variables
    load_dotenv()

    # Initialize Twitter client using tweepy
    client = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )

    try:
        # Post the tweet using tweepy
        response = client.create_tweet(text=tweet)
        print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
        return True, response.data['id']
    except (TooManyRequests, TwitterServerError) as e:
        print(f"Twitter rate limit or server error: {e}. Waiting...")
        time.sleep(60)  # Wait for 60 seconds before retrying
        return False, None
    except Exception as e:
        print(f"Failed to post tweet: {e}")
        return False, None

if __name__ == "__main__":
    topic = input("Enter a topic for the tweet: ")
    tweet = generate_tweet_from_topic(topic)
    post_tweet(tweet)