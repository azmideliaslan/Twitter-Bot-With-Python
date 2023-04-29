import requests
import tweepy
from googletrans import Translator
import datetime
import os

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
producthunt_access_token = os.environ.get("PRODUCTHUNT_ACCESS_TOKEN")

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
response = requests.post(url, headers={"Authorization": f"Bearer {producthunt_access_token}"}, json={"query": query})

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
      tweet = client.create_tweet(text=tweet_text)
      print({tweet_text})
      fst = fst + 1
else:
  # Handle error
  print("API request failed")
  print(response.status_code, response.reason, response.content)
