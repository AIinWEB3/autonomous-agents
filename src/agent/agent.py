import ast
import datetime
import os
import logging
from dotenv import load_dotenv
from pprint import pformat
from .agent_tools.data import Data
from .agent_tools.model import Model
from .agent_config.config import Config
from tweepy.errors import TooManyRequests

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

class Agent:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Initialize config
        self.config = Config()

        # Initialize model
        self.model = Model(
            api_key=os.getenv("MODEL_API_KEY"),
            url=os.getenv("MODEL_URL"),
            model=os.getenv("MODEL_NAME")
        )

        # Initialize empty data
        self.data = {}

        # Set up logging
        self.logger = logging.getLogger(__name__)

    def set_topics(self, topics):
        """Sets the list of topics for the agent to post about."""
        self.topics = topics

    def __construct_data_prompt(self):
        return self.config.data_prompt + pformat(self.data)

    def __construct_post_prompt(self):
        """Constructs the post prompt using the list of topics."""
        return self.config.purpose_prompt + self.config.post_prompt + str(self.topics)

    def __construct_repsonse_prompt(self, conversation):
        return self.config.purpose_prompt + self.config.reply_prompt + pformat(conversation)
    
    def __process_data(self):
        try:
            prompt = self.__construct_data_prompt()
            logging.info("Processing data with LLM...")
            response = self.model.query(prompt)
            logging.info("Data processed successfully")
            return response
        except Exception as e:
            logging.error(f"Error processing data: {e}")
            return None

    # Comment out Twitter-related methods for now
    """
    def __get_threads(self, conversation_ids):
        pass

    def __get_relevant_conversations(self):
        pass

    def __respond_to_conversation(self, conversation):
        pass

    def respond_to_key_users(self):
        pass

    def post_tweet(self):
        pass
    """

    def respond_to_key_users(self):
        # Example logic to respond to key users
        conversations = self.twitter.get_relevant_conversations()
        for conversation in conversations:
            # Determine if a response is needed
            if self.should_respond(conversation):
                self.twitter.post_tweet("Responding to a key user!")

def main():
    try:
        logging.info("Agent starting up...")
        agent = Agent()
        
        # Process data and generate response
        processed_data = agent.__process_data()
        if processed_data:
            logging.info("Generated response:")
            print(processed_data)
        else:
            logging.error("Failed to process data")
        
        logging.info("Agent shutting down...")
    except Exception as e:
        logging.error(f"Agent error: {e}")
    except KeyboardInterrupt:
        logging.info("Agent shutting down (interrupted by user)...")


if __name__ == "__main__":
    main()
