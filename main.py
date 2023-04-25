import requests
import json

# OAuth2 access token
access_token = "dS0dChIGxjE17GL-9MClHorAntWimIdklS9EWYeWo48"

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

# API request
response = requests.post(url, headers={"Authorization": f"Bearer {access_token}"}, json={"query": query})

# Check if request was successful
if response.ok:
  # Parse response data
  data = response.json().get("data", {}).get("posts", {}).get("edges", [])

  # Process or use data
  for posts in data:
    node = posts.get("node", {})
    print(node.get("name"), node.get("tagline"), node.get("votesCount"))
else:
  # Handle error
  print("API request failed")
  print(response.status_code, response.reason, response.content)
