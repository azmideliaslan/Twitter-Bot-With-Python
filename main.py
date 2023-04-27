import requests
import tweepy

# OAuth2 producthunt access token
access_token_producthunt = "dS0dChIGxjE17GL-9MClHorAntWimIdklS9EWYeWo48"

# API anahtarları ve erişim belirteçlerinizi buraya girin
consumer_key = "yUgnOqtKuk0RRaqI9K6VPxf95"
consumer_secret = "kZozbEljHCnXB5GfmprQKwMiOKBrdqBmAd9ikFFbmliH3MiYw0"
access_token = "1650782110272090113-vRIf8zp1JS0ow45xWyV1nhFnnt5JH8"
access_token_secret = "wEDymbqQszxyE1q3lAChDMHadAx86l8oiVxkgiEJDuYUI"

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
          name
          tagline
          description
          media {
            videoUrl
            
          }
          topics {
            edges {
              node {
                name
              }
            }
          }
          votesCount
          url
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
      tweet_text = f"{node.get('name')} - {node.get('tagline')} ({node.get('votesCount')} votes)"
      media_url = None  # replace this with the URL of the image you want to attach to the tweet
      tweet = client.create_tweet(text=tweet_text, media_ids=[media_url] if media_url else None)
      print(tweet_text)
else:
  # Handle error
  print("API request failed")
  print(response.status_code, response.reason, response.content)
