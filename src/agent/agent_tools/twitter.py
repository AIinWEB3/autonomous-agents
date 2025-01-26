import tweepy
from pprint import pp
import time
from tweepy.errors import TooManyRequests, TwitterServerError

class Twitter:
    """A class for interfacing with the Twitter API using Tweepy.

    Attributes:
        client (tweepy.Client): The authenticated Tweepy client instance for
            interacting with the Twitter API.
        user_id (str): The ID of the authenticated Twitter user.
    
    Methods:
        get_relevant_conversations(key_users, conversation_ids, start_time):
            Retrieves tweets from specified users or with particular 
            conversation ids and groups them by conversation ID.

        post_tweet(post_text, in_reply_to_tweet_id):
            Posts a new tweet. If `in_reply_to_tweet_id` is not `None` then it 
            posts a reply to the tweet specific by `in_reply_to_tweet_id`.
    """


    def __init__(
            self,
            api_key: str,
            api_secret: str,
            access_token: str,
            access_token_secret: str,
            bearer_token: str):
        """
        Initializes the Twitter class with with the necessary parameters.

        Args:
            api_key (str): The API key for OAuth 1.0a authentication.
            api_secret (str): The API secret for OAuth 1.0a authentication.
            access_token (str): The access token for OAuth 1.0a authentication.
            access_token_secret (str): The access token secret for OAuth 1.0a
                authentication.
            bearer_token (str, optional): The Bearer token for OAuth 2.0
                authentication.

        Sets up the Tweepy client for both OAuth 1.0a and OAuth 2.0 
        authentication and retrieves the authenticated user's ID.
        """
        self.v2api = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            return_type = dict
        )
        self.user_id = self.v2api.get_me()["data"]["id"]


    def __build_search_query_users(self, key_users):
        """Returns a twitter search query for the provided list of users"""
        return "(from:" + " OR from:".join(key_users) + ")"


    def __build_search_query_conversations(self, conversation_ids):
        """Returns a twitter search query for the provided list of users"""
        return "(conversation_id:" + " OR conversation_id:".join(conversation_ids) + ")"


    def get_relevant_conversations(self, hours_ago=2):
        max_retries = 3
        base_delay = 60  # Start with 60 second delay
        
        for attempt in range(max_retries):
            try:
                response = self.v2api.search_recent_tweets(
                    query=self.search_query,
                    max_results=100,
                    tweet_fields=['author_id', 'created_at', 'conversation_id'],
                    start_time=self._get_time_hours_ago(hours_ago),
                    expansions=['author_id', 'referenced_tweets.id']
                )
                return response
                
            except TooManyRequests as e:
                if attempt == max_retries - 1:  # Last attempt
                    print(f"Rate limit exceeded after {max_retries} attempts. Giving up.")
                    raise e
                    
                delay = base_delay * (2 ** attempt)  # Exponential backoff
                print(f"Rate limit hit. Waiting {delay} seconds before retry {attempt + 1}/{max_retries}...")
                time.sleep(delay)
                continue
                
            except TwitterServerError as e:
                print(f"Twitter server error: {e}")
                if attempt == max_retries - 1:
                    raise e
                time.sleep(base_delay)
                continue
                
            except Exception as e:
                print(f"Unexpected error: {e}")
                raise e

    def _get_time_hours_ago(self, hours):
        """Helper method to get datetime object for hours ago"""
        from datetime import datetime, timedelta
        return (datetime.utcnow() - timedelta(hours=hours)).isoformat('T') + 'Z'


    def post_tweet(self, post_text, in_reply_to_tweet_id=None):
        """Posts a new tweet or a reply to the specified tweet."""
        try:
            response = self.v2api.create_tweet(
                in_reply_to_tweet_id=in_reply_to_tweet_id,
                text=post_text
            )
            return (True, response["data"]["id"])
        except Exception as e:
            print(f"Error posting reply: {e}")
            return (False, None)
