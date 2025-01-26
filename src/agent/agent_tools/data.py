import datetime
import requests
import os
from .twitter import Twitter

class Data:
    """
    A class for gathering relevant data for the twitter agent.

    In this example it fetches real-time data from Twitter and CryptoPanic. The
    class can be reconfigured to fetch any data relevant to the agent.

    Attributes:
        PERIOD (int): Will fetch fetch news from the past `PERIOD` hours.

    Methods:
        get_data: Returns a dictionary containing the fetched data.
    """
    CRYPTO_NEWS=[
        "CoinDesk",
        "CoinGecko",
        "Cointelegraph",
        "crypto",
        "decryptmedia",
        "DefiantNews",
        "TheBlock__",
        "WatcherGuru",
        "whale_alert"
    ]

    KOLS=[
        "aixbt",
        "AltcoinDailyio",
        "AltcoinGordon",
        "CryptoWizardd",
        "KoroushAK",
        "loomdart",
        "Trader_XO",
        "Trader_Jibon",
        "Tradermayne",
        "WhalePanda"
    ]

    # Will fetch fetch news from the past `PERIOD` hours
    PERIOD=2

    def __init__(self, clients, keys):
        """
        Initializes the Data class with clients and keys.

        Args:
            clients (dict): A dictionary containing the relevant client objects.
            keys (dict): A dictionary containing the relevant API keys.
        """
        self.twitter = clients["twitter"]
        self.crypto_panic_key = keys["crypto_panic"]
        self.start_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=self.PERIOD)


    def __get_twitter_data(self):
        """Fetches relevant cryptocurrency-related tweets."""
        key_users = self.CRYPTO_NEWS + self.KOLS
        return self.twitter.get_relevant_conversations(
            key_users=key_users,
            start_time=self.start_time)
    

    def __get_crypto_panic_data(self):
        """Fetches posts from the CryptoPanic API."""
        try:
            response = requests.get(
                "https://cryptopanic.com/api/v1/posts/",
                params={"auth_token": os.getenv("CRYPTO_PANIC_API_KEY"), "public": "true"}
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            
            if "results" not in data:
                print("Warning: No 'results' key in CryptoPanic API response")
                return []
            
            return [result["title"] for result in data["results"]]
        except requests.RequestException as e:
            print(f"Error fetching CryptoPanic data: {e}")
            return []
        except KeyError as e:
            print(f"Unexpected API response structure: {e}")
            return []


    def get_data(self):
        """
        Fetches data from the relevant sources.
        
        Called once when agent starts up.
        """

        twitter_data = self.__get_twitter_data()
        crypto_panic_data = self.__get_crypto_panic_data()
        
        return {
            "twitter_data": twitter_data,
            "crypto_panic_data": crypto_panic_data
        }

