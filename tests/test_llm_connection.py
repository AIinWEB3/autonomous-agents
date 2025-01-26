import unittest
import os
from dotenv import load_dotenv
from openai import OpenAI

class TestLLMConnection(unittest.TestCase):
    def setUp(self):
        # Load environment variables
        load_dotenv()
        
        # Get credentials from environment variables
        self.model_url = os.getenv("MODEL_URL")
        self.model_api_key = os.getenv("MODEL_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", 
            "accounts/sentientfoundation/models/dobby-mini-unhinged-llama-3-1-8b#accounts/sentientfoundation/deployments/81e155fc")
        
        # Initialize the client
        self.client = OpenAI(
            base_url=self.model_url,
            api_key=self.model_api_key
        )

    def test_llm_credentials(self):
        """Test that all required credentials are present"""
        self.assertIsNotNone(self.model_url, "MODEL_URL is missing")
        self.assertIsNotNone(self.model_api_key, "MODEL_API_KEY is missing")
        self.assertIsNotNone(self.model_name, "MODEL_NAME is missing")

    def test_llm_connection(self):
        """Test LLM API connection"""
        try:
            # Create the completion request
            messages = [
                {"role": "user", "content": "Tell me something unhinged!"}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=100
            )
            
            # Get the response
            message = response.choices[0].message.content
            self.assertIsNotNone(message)
            self.assertGreater(len(message), 0)
            print(f"\nGenerated text: {message}")
            
        except Exception as e:
            self.fail(f"LLM connection failed: {str(e)}")

if __name__ == '__main__':
    unittest.main() 