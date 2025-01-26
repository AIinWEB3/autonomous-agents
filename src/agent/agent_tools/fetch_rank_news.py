import requests
import os
from dotenv import load_dotenv
from src.agent.agent_tools.model import Model

def get_ranked_news(num_news=5):
    # Load environment variables
    load_dotenv()
    
    # Get auth token from environment variable
    auth_token = os.getenv("CRYPTOPANIC_AUTH_TOKEN")
    if not auth_token:
        print("Error: CRYPTOPANIC_AUTH_TOKEN not found in .env file")
        return
    
    # Initialize the model
    model = Model(
        api_key=os.getenv("MODEL_API_KEY"),
        url=os.getenv("MODEL_URL"),
        model=os.getenv("MODEL_NAME")
    )
    
    # Define the API endpoint
    api_url = "https://cryptopanic.com/api/v1/posts/"
    
    # Construct the full URL with the auth token and limit
    full_url = f"{api_url}?auth_token={auth_token}&public=true&limit={num_news}"
    
    try:
        # Make a GET request to the API
        response = requests.get(full_url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                news_items = data['results'][:num_news]
                ranked_news = []
                
                for news in news_items:
                    # Construct prompt for analysis
                    prompt = f"""
                    Analyze this crypto news item and rate its potential value on a scale of 1-100:
                    Title: {news.get('title')}
                    URL: {news.get('url')}
                    
                    Please provide:
                    1. Value score (1-100)
                    2. Brief explanation (1 sentence)
                    
                    Format your response as:
                    Value: [score]
                    Explanation: [brief analysis]
                    """
                    
                    # Debug: Print the prompt
                    print(f"Prompt for news '{news.get('title')}': {prompt}")
                    
                    analysis = model.query(prompt)
                    
                    # Debug: Print the raw analysis result
                    print(f"Raw analysis for news '{news.get('title')}': {analysis}")
                    
                    # Extract the value score from the analysis
                    try:
                        score_line = next(line for line in analysis.split('\n') if line.startswith('Value:'))
                        score = int(score_line.split(': ')[1].strip())
                    except (StopIteration, ValueError, IndexError) as e:
                        print(f"Error extracting score for news '{news.get('title')}': {e}")
                        score = 0  # Default score if extraction fails
                    
                    # Add analysis and score to news item
                    news['analysis'] = analysis
                    news['score'] = score
                    ranked_news.append(news)
                
                # Sort by value score
                ranked_news.sort(key=lambda x: x['score'], reverse=True)
                
                # Debug: Print the sorted scores
                print("Sorted scores:")
                for news in ranked_news:
                    print(f"Title: {news.get('title')}, Score: {news['score']}")
                
                # Print ranked news
                print("\n=== Ranked Crypto News by Value ===\n")
                for i, news in enumerate(ranked_news, 1):
                    print(f"\n{i}. {news.get('title')}")
                    print(f"Published At: {news.get('published_at')}")
                    print(f"URL: {news.get('url')}")
                    print("\nAnalysis:")
                    print(news['analysis'])
                
                return ranked_news
            else:
                print("No news items found.")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    ranked_news = get_ranked_news(5)
    
    # Optionally post educational tweet about top news
    post_tweet = input("\nWould you like to post an educational tweet about the top news? (y/n): ")
    if post_tweet.lower() == 'y':
        from src.agent.agent_tools.top_news_tweet import post_educational_tweet
        post_educational_tweet()