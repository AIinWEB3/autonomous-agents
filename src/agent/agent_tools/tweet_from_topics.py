import os
import tweepy
from pprint import pp
import time
from tweepy.errors import TooManyRequests, TwitterServerError
from dotenv import load_dotenv
from src.agent.agent_tools.model import Model
from src.agent.agent_tools.topics import TOPICS  # Import the topics

LAST_CONCEPT_FILE = "last_concept.txt"

def get_last_concept_index():
    """Retrieve the last concept index from a file."""
    if os.path.exists(LAST_CONCEPT_FILE):
        with open(LAST_CONCEPT_FILE, 'r') as file:
            return int(file.read().strip())
    return -1

def set_last_concept_index(index):
    """Store the last concept index in a file."""
    with open(LAST_CONCEPT_FILE, 'w') as file:
        file.write(str(index))

def generate_tweet_from_concept(concept, model):
    """Generate a tweet for a given concept."""
    prompt = f"""Explain {concept} in crypto with these requirements:
    1. Use simple language a beginner can understand
    2. Be bold and direct
    3. Include a real-world example or analogy
    4. Keep it under 240 characters
    
    Format: [Concept explanation] + [Example/Analogy]"""
    
    response = model.query(prompt)
    
    tweet = f"""🔥 Crypto Knowledge Drop: {concept}

{response}

#Crypto #Web3 #CryptoEducation"""
    
    return tweet

def post_tweet(tweet):
    """Post a tweet using the Twitter API."""
    load_dotenv()
    client = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )
    try:
        response = client.create_tweet(text=tweet)
        print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
        print("\nTweet content:")
        print(tweet)
        return True
    except tweepy.errors.TooManyRequests:
        print("Rate limit exceeded. Waiting...")
        return False
    except Exception as e:
        print(f"Failed to post tweet: {e}")
        return False

def main():
    # Ensure last_concept.txt exists
    if not os.path.exists(LAST_CONCEPT_FILE):
        with open(LAST_CONCEPT_FILE, 'w') as f:
            f.write("-1")
    
    load_dotenv()
    model = Model(
        api_key=os.getenv("MODEL_API_KEY"),
        url=os.getenv("MODEL_URL"),
        model=os.getenv("MODEL_NAME"),
        temperature=0.7
    )

    last_index = get_last_concept_index()
    
    try:
        while True:
            next_index = (last_index + 1) % len(TOPICS)
            concept = TOPICS[next_index]  # Access the concept using the index
            
            print(f"\nGenerating tweet for concept: {concept}")
            tweet = generate_tweet_from_concept(concept, model)
            
            if post_tweet(tweet):
                set_last_concept_index(next_index)
                last_index = next_index
                print("Waiting 6 hours before next tweet...")
                time.sleep(21600)  # Wait 6 hours between tweets
            else:
                print("Tweet failed. Retrying in 15 minutes...")
                time.sleep(900)  # Wait 15 minutes before retry
                
    except KeyboardInterrupt:
        print("\nStopping the tweet bot...")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    main()