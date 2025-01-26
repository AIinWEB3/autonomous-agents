import os
import tweepy
import time
from dotenv import load_dotenv
from tweepy.errors import TooManyRequests, TwitterServerError
from src.agent.agent_tools.model import Model
from src.agent.agent_tools.fetch_rank_news import get_ranked_news

LAST_POSTED_FILE = "last_posted_news.txt"

# Ensure the file exists
if not os.path.exists(LAST_POSTED_FILE):
    with open(LAST_POSTED_FILE, 'w') as file:
        file.write("")  # Initialize with an empty string or a specific identifier

def get_last_posted_news():
    """Retrieve the last posted news identifier from a file."""
    if os.path.exists(LAST_POSTED_FILE):
        with open(LAST_POSTED_FILE, 'r') as file:
            return file.read().strip()
    return None

def set_last_posted_news(news_identifier):
    """Store the last posted news identifier in a file."""
    with open(LAST_POSTED_FILE, 'w') as file:
        file.write(news_identifier)

def extract_key_concept(news_item, model):
    """Extract the key crypto concept from a news item."""
    prompt = f"""
    From this crypto news:
    Title: {news_item.get('title')}
    Description: {news_item.get('description')}
    
    1. Identify the most important 1-3 word crypto concept that a beginner should understand
    2. Write a brief, beginner-friendly explanation using this news as an example
    
    Format your response exactly as:
    Concept: [1-3 word concept]
    Example: [1 sentence explanation using this news]
    """
    
    return model.query(prompt)

def create_tweet(news_item, concept_analysis):
    """Create a tweet from the news and concept analysis with a bold, unapologetic tone."""
    concept = [line for line in concept_analysis.split('\n') if line.startswith('Concept:')][0].replace('Concept:', '').strip()
    example = [line for line in concept_analysis.split('\n') if line.startswith('Example:')][0].replace('Example:', '').strip()
    
    tweet = f"""🔥 SatoshiSavage Alert: {concept} is shaking things up!

📰 {example}

🔗 {news_item.get('url')}

Tone: SatoshiSavage's tone should be like your drunk uncle at Thanksgiving—unfiltered, straight-up, and full of fuck-you energy. Raw, unapologetic, and always pushing the decentralization narrative. No sugarcoating, no fluff, just brutal honesty and a side of humor. If you can't handle the heat, stay the fuck out of the crypto game. 💥"""

    return tweet

def post_educational_tweet():
    # Load environment variables
    load_dotenv()
    
    # Initialize the model
    model = Model(
        api_key=os.getenv("MODEL_API_KEY"),
        url=os.getenv("MODEL_URL"),
        model=os.getenv("MODEL_NAME"),
        temperature=0.7  # Adjust temperature for more variability
    )
    
    # Get the top ranked news
    ranked_news = get_ranked_news(5)
    if not ranked_news:
        print("No news available to tweet about")
        return
    
    # Get the top news item
    top_news = ranked_news[0]
    top_news_identifier = top_news.get('url')  # Use URL or another unique identifier
    
    # Check if the top news is the same as the last posted news
    last_posted_news = get_last_posted_news()
    if top_news_identifier == last_posted_news:
        print("Top news is the same as the last posted news. Skipping tweet.")
        return
    
    # Extract key concept and create tweet
    concept_analysis = extract_key_concept(top_news, model)
    tweet_text = create_tweet(top_news, concept_analysis)
    
    # Initialize Twitter client
    client = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )
    
    try:
        # Post the tweet
        response = client.create_tweet(text=tweet_text)
        print("Educational tweet posted successfully!")
        print("\nTweet content:")
        print(tweet_text)
        
        # Update the last posted news
        set_last_posted_news(top_news_identifier)
        
        return True, response.data['id']
    except (TooManyRequests, TwitterServerError) as e:
        print(f"Twitter rate limit or server error: {e}. Waiting...")
        time.sleep(60)
        return False, None
    except Exception as e:
        print(f"Failed to post tweet: {e}")
        return False, None

if __name__ == "__main__":
    post_educational_tweet()
