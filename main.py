import requests
import tweepy

# OAuth2 producthunt access token
access_token_producthunt = "dS0dChIGxjE17GL-9MClHorAntWimIdklS9EWYeWo48"

# API anahtarları ve erişim belirteçlerinizi buraya girin
consumer_key = "TTSp8LeRV8P6w2xYStRHqeFPs"
consumer_secret = "roUMN1Qh6Duh15JvbJMYtoe0SY7kMXTYRiF5AsBBUnKpwvz0Rn"
access_token = "879512133557420032-3aeJKPHUYIX1FG4ilzW7zJcLZXQP6cU"
access_token_secret = "8IOy0mE027XHLoU9ZB5WBsGWCaMVsYfAOSJ0ZEWv202uf"

#twitter atturatize
client = tweepy.Client(consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token=access_token,
                    access_token_secret=access_token_secret)
# API endpoint
url = "https://api.producthunt.com/v2/api/graphql/"

# GraphQL query
query = """
  query {
    posts( first: 3 ){
      edges {
        node {
          id
          name
          tagline
          votesCount
        }
      }
    }
  }

"""

# API request producthunt
response = requests.post(url, headers={"Authorization": f"Bearer {access_token_producthunt}"}, json={"query": query})

# Check if request was successful
if response.ok:
  # Parse response data
  data = response.json().get("data", {}).get("posts", {}).get("edges", [])

  # Process or use data
  for posts in data:
    node = posts.get("node", {})
    tweet = client.create_tweet(text=node.get("name"))
    print(node.get("name"), node.get("tagline"), node.get("votesCount"))
else:
  # Handle error
  print("API request failed")
  print(response.status_code, response.reason, response.content)
