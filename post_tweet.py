import tweepy

# API anahtarları ve erişim belirteçlerinizi buraya girin
consumer_key = "TTSp8LeRV8P6w2xYStRHqeFPs"
consumer_secret = "roUMN1Qh6Duh15JvbJMYtoe0SY7kMXTYRiF5AsBBUnKpwvz0Rn"
access_token = "879512133557420032-3aeJKPHUYIX1FG4ilzW7zJcLZXQP6cU"
access_token_secret = "8IOy0mE027XHLoU9ZB5WBsGWCaMVsYfAOSJ0ZEWv202uf"

client = tweepy.Client(consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token=access_token,
                    access_token_secret=access_token_secret)
response = client.create_tweet(text='hello world')
