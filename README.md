# 🤖 SatoshiSavage

SatoshiSavage is an autonomous Twitter agent on a mission to educate people about crypto, Web3, and blockchain. Think of it as the unapologetic drunk uncle at Thanksgiving—unfiltered, straight-shooting, and brimming with fiery energy. It's raw, bold, and relentlessly champions the decentralization narrative. No sugarcoating, no fluff—just brutal honesty with a side of sharp humor. If you can't handle the heat, maybe the crypto world isn't for you.

## 🔥 Core Features

### News-Driven Education (`top_news_tweet.py`)
- Automatically fetches and processes latest crypto news
- Extracts key educational concepts from headlines
- Generates savage, beginner-friendly explanations
- Posts tweets with source links for deeper learning
- Tracks posted news to avoid duplicates

### 💡 Systematic Education (`tweet_from_topics.py`)
- Works through 100+ essential crypto topics
- Generates educational tweets with real-world examples
- Maintains the signature unhinged but informative tone
- Topics include:
  - Blockchain Fundamentals
  - DeFi & Trading
  - Security & Privacy
  - Emerging Tech
  - And more savage knowledge bombs

### 🤖 Technical Components
- **fetch_rank_news.py**: News gathering and ranking system
- **topics.py**: Comprehensive crypto topic dictionary
- **model.py**: AI integration for content generation
  - OpenAI-compatible API interface
  - Customizable temperature for tone control
  - Consistent personality maintenance

## 🚀 Getting Started

## 🦄 X Agent Features:
* Makes posts after fetching data from news sources 📰
* Responds to Tweets from specified users 🌶️
* Supports any OpenAI API compatible LLM endpoint 🔥
* Highly flexible, just change `agent_config` and `agent_tools` 🧠
* It works 😎

# 🚀 Quickstart

## Setting Up Credentials 🔐

### 1.&nbsp;&nbsp;Create secrets file

Create the `.env` file by copying the contents of `.env.example`. This is where you will store all of your agent's credentials.
```
cp .env.example .env
```

### 2.&nbsp;&nbsp;Get X credentials
> [!WARNING]
> **We suggest creating a new X account for your agent.**

In order to interact with the X platform, your agent needs X developer credentials from the X developer portal [here](https://developer.x.com/en/portal/dashboard).

From the *Dashboard* page, click on the gear icon to access the *Settings* page for your default project.

Set the user authentication settings for your app as follows:
- App permissions: "Read and write"
- Type of App: "Web App, Automated App or Bot"
- Callback URI / Redirect URL: http://localhost:8000
- Website URL: http://example.com

Generate all of the required credentials on the *Keys and tokens* page. Add them to the `.env` file.

### 3.&nbsp;&nbsp;Get model inference credentials
Add your Fireworks or other inference provider base url, model name and API key to the `.env` file.

## Running Locally 💻
> [!NOTE]
> **Before you proceed, make sure that you have installed `python` and `pip`. If you have not, follow [these](https://packaging.python.org/en/latest/tutorials/installing-packages/) instructions to do so.**

### 1.&nbsp;&nbsp;Create a Python virtual environment
On Unix / MacOS:
```
python -m venv .venv
```

On Windows:
```
py -m venv .venv
```

### 2.&nbsp;&nbsp;Activate the Python virtual environment
On Unix / MacOS:
```
source .venv/bin/activate
```

On Windows:
```
.venv\Scripts\activate
```

### 3.&nbsp;&nbsp;Install dependencies
```
pip install -r requirements.txt
```

### 4.&nbsp;&nbsp;Run tests
```
python -m unittest -v
```

### 5.&nbsp;&nbsp;Run your agent
```
python -m src.agent.agent
```

## ⚙️ Configuring your agent
### Giving your agent a purpose and personality 🌶️
You can congifure your agent's personality by updating the prompt files in the `agent_config` package in `src/agent/agent_config/prompts`.
- `purpose_prompt.txt` is used to tell the agent the purpose that it serves.
- `data_prompt.txt` is used to tell the agent how to process the data that it uses to inform its posts.
- `post_prompt.txt` is used to tell the agent how to post a new tweet (tone, format, etc).
- `reply_prompt.txt` is used to tell the agent how to reply to a key user's tweet (tone, format, etc).

<p align="left">
  <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExeHdrNzJpNjl0eGNzdGVxYWk4cG1pMDFsYjd5bmh3eWV3aHNnOW55cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Pu5F5t64WNKYE/giphy.gif" alt="Purpose" width="60%"/>
</p>

### Picking which users your agent interacts with 🤜🤛
You can configure your agent to respond to particular key users using the `KEY_USERS` constant in the `agent` module in `src/agent/agent.py`. Your agent will respond to tweets from these key users.

### Picking the data your agent uses 📊
You can configure the data that your agent has access to using using the `data` module in the `agent_tools` package in `src/agent/agent_tools/data.py`.

# 🧐 Technical Information

## X API
> [!NOTE]
> **It is important to consider X API [rate limits](https://docs.x.com/x-api/fundamentals/rate-limits#v2-limits). In this example, every time the agent runs, three calls are made to the [Recent Search](https://docs.x.com/x-api/posts/recent-search) endpoint, which is not possible with the free plan (you would need to wait 15 minutes between calls).** 

If you are using the free plan, you would more than likely need to choose between responding to particular users' post and using X as a data source. You can use other endpoints to fetch posts, mentions, reposts and quotes that have their own rate limits, but managing different endpoints' rate limits significantly complicates development. These are the endpoints that this agent uses:

### Post a tweet
- Endpoint: `POST /2/tweets`
- Documentation:
    - https://docs.x.com/x-api/posts/creation-of-a-post
- Rate limits:
    - Free: 17 requests / 24 hours
    - Basic ($200/month): 100 requests / 24 hours
    - Pro ($5000/month): 100 requests / 15 minutes

### Search for tweets
- Endpoint: `GET /2/tweets/search/recent`
- Documentation:
    - https://docs.x.com/x-api/posts/recent-search
    - https://docs.x.com/x-api/posts/search/integrate/build-a-query
- Rate limits:
    - Free: 1 requests / 15 minutes
    - Basic ($200/month): 60 requests / 15 mins
    - Pro ($5000/month): 300 requests / 15 mins

## 💡 Usage

Run either bot:
```bash
# For news-based education
python -m src.agent.agent_tools.top_news_tweet

# For systematic topic coverage
python -m src.agent.agent_tools.tweet_from_topics
```
