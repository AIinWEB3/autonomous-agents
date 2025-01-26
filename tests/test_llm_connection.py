import os
from dotenv import load_dotenv
from openai import OpenAI

def test_llm_connection():
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    model_url = os.getenv("MODEL_URL")
    model_api_key = os.getenv("MODEL_API_KEY")
    model_name = os.getenv("MODEL_NAME", 
        "accounts/sentientfoundation/models/dobby-mini-unhinged-llama-3-1-8b#accounts/sentientfoundation/deployments/81e155fc")
    
    # Verify all credentials are present
    if not all([model_url, model_api_key]):
        raise ValueError("Missing required LLM credentials in environment variables")
    
    try:
        # Initialize the client
        client = OpenAI(
            base_url=model_url,
            api_key=model_api_key
        )
        
        # Create the completion request
        messages = [
            {"role": "user", "content": "Tell me something unhinged!"}
        ]
        
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.7,
            max_tokens=100
        )
        
        # Get the response
        message = response.choices[0].message.content
        print("\nGenerated text:", message)
        return True
            
    except Exception as e:
        print(f"Connection Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_llm_connection()
    if success:
        print("\nLLM API connection successful! ✅")
    else:
        print("\nLLM API connection failed! ❌") 