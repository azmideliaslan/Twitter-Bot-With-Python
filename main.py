import requests
import tweepy
from googletrans import Translator
import datetime

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

# Initialize Translator
translator = Translator()
# Şu anki tarih ve saat
now = datetime.datetime.now()
#Günü alıyorum
day_name = now.strftime("%d %B")
tr_day_name = translator.translate(day_name,dest='tr').text

# API request producthunt
response = requests.post(url, headers={"Authorization": f"Bearer {access_token_producthunt}"}, json={"query": query})

# Check if request was successful
if response.ok:
  # Parse response data
  data = response.json().get("data", {}).get("posts", {}).get("edges", [])
  fst = 1

  for posts in data:
      node = posts.get("node", {})
      name = node.get("name")
      tagline = node.get("tagline")
      description = node.get("description")
      topics = [topic.get("node", {}).get("name", "").replace(" ", "") for topic in node.get("topics", {}).get("edges", [])]
      votes_count = node.get("votesCount")
      url = node.get("url")

      # Türkçe'ye çevirme
      tr_tagline = translator.translate(tagline,dest='tr').text
      tr_description = translator.translate(description,dest='tr').text
      tr_topics = [translator.translate(topic,dest='tr').text.replace(" ", "") for topic in topics]
      # Tweet oluşturma
      first_tweet_content = f"{tr_day_name} En Popüler Dijital Ürünleri #{fst}\n"
      tweet_text = f"{first_tweet_content}{name} - {tr_tagline}\n\n\n\n Oy sayısı: {votes_count} \n\n #{tr_topics[0]} #{tr_topics[1]} #{topics[0]} #{topics[1]} #ProductHunt \n\n{url}\n\n"
      #Tanım eklenebilirse ekliyorum (bir twit 400 karakteri geçmemeli)
      if len(tweet_text) + len(tr_description) <= 400:
          tweet_text = f"{first_tweet_content}{name} - {tr_tagline} - {tr_description}\n\n\n\n Oy sayısı: {votes_count} \n\n #{tr_topics[0]} #{tr_topics[1]} #{topics[0]} #{topics[1]} #ProductHunt\n\n{url}\n\n"
          print("sda  len(tweet_text)")
      else:
          print(len(tweet_text))
      #tweet = client.create_tweet(text=tweet_text)
      print({tweet_text})
      fst = fst + 1
else:
  # Handle error
  print("API request failed")
  print(response.status_code, response.reason, response.content)
