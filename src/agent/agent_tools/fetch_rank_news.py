import requests
import os
from dotenv import load_dotenv
from src.agent.agent_tools.model import Model

def get_ranked_news(num_news=5):
    load_dotenv()
    auth_token = os.getenv("CRYPTOPANIC_AUTH_TOKEN")
    if not auth_token:
        print("Error: CRYPTOPANIC_AUTH_TOKEN not found in .env file")
        return
    
    model = Model(
        api_key=os.getenv("MODEL_API_KEY"),
        url=os.getenv("MODEL_URL"),
        model=os.getenv("MODEL_NAME")
    )
    
    api_url = "https://cryptopanic.com/api/v1/posts/"
    full_url = f"{api_url}?auth_token={auth_token}&public=true&limit={num_news}"
    
    try:
        response = requests.get(full_url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                news_items = data['results'][:num_news]
                ranked_news = []
                
                for news in news_items:
                    # Enhanced prompt with more context and specific criteria
                    prompt = f"""
                    Analyze this crypto news item and rate its potential impact and value on a scale of 1-100.
                    
                    News Details:
                    - Title: {news.get('title')}
                    - URL: {news.get('url')}
                    - Published: {news.get('published_at')}
                    
                    Consider these factors in your scoring:
                    - Market Impact (1-25): How much could this affect crypto markets?
                    - Innovation/Technology (1-25): Does this involve technological advancement?
                    - Adoption/Usage (1-25): Will this increase crypto adoption or usage?
                    - Regulatory/Risk (1-25): Are there regulatory or risk implications?
                    
                    Format your response exactly as follows:
                    Market Impact Score: [number]
                    Innovation Score: [number]
                    Adoption Score: [number]
                    Risk Score: [number]
                    Total Value: [sum of all scores]
                    Explanation: [1-2 sentence analysis]
                    """
                    
                    analysis = model.query(prompt)
                    print(f"\nRaw analysis for '{news.get('title')}': {analysis}")
                    
                    # Enhanced score extraction
                    try:
                        # Extract individual component scores
                        lines = analysis.split('\n')
                        scores = {}
                        for line in lines:
                            if 'Score:' in line:
                                category, value = line.split('Score:')
                                scores[category.strip()] = int(value.strip())
                            elif 'Total Value:' in line:
                                total_score = int(line.split(':')[1].strip())
                            elif 'Explanation:' in line:
                                explanation = line.split(':')[1].strip()
                        
                        # Validate total score
                        calculated_total = sum(scores.values())
                        if abs(calculated_total - total_score) > 1:  # Allow for minor rounding differences
                            print(f"Warning: Score mismatch. Calculated: {calculated_total}, Reported: {total_score}")
                            total_score = calculated_total
                        
                    except Exception as e:
                        print(f"Error extracting scores: {e}")
                        total_score = 0
                        explanation = "Score extraction failed"
                    
                    news['analysis'] = analysis
                    news['score'] = total_score
                    news['detailed_scores'] = scores
                    news['explanation'] = explanation
                    ranked_news.append(news)
                
                # Sort by value score
                ranked_news.sort(key=lambda x: x['score'], reverse=True)
                
                # Print ranked news with detailed breakdown
                print("\n=== Ranked Crypto News by Value ===\n")
                for i, news in enumerate(ranked_news, 1):
                    print(f"\n{i}. {news.get('title')}")
                    print(f"Published At: {news.get('published_at')}")
                    print(f"URL: {news.get('url')}")
                    print("\nScore Breakdown:")
                    for category, score in news.get('detailed_scores', {}).items():
                        print(f"- {category}: {score}")
                    print(f"Total Score: {news['score']}")
                    print(f"Explanation: {news.get('explanation')}")
                
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
    
    post_tweet = input("\nWould you like to post an educational tweet about the top news? (y/n): ")
    if post_tweet.lower() == 'y':
        from src.agent.agent_tools.top_news_tweet import post_educational_tweet