import datetime
import requests
import os

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

    def __init__(self, apis, keys):
        """
        Initialize the Data class.
        
        Args:
            apis (dict): Dictionary of API objects (like Twitter client)
            keys (dict): Dictionary of API keys (like CryptoPanic API key)
        """
        self.apis = apis
        self.keys = keys
        self.crypto_panic_key = keys.get("crypto_panic")
        self.start_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=self.PERIOD)

    def get_data(self):
        """
        Fetches data from the relevant sources.
        
        Called once when agent starts up.
        """
        return {}
