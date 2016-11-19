#!/usr/bin/python3

from omekaclient import OmekaClient
with open('key') as f:
    api_key = f.readline()[:-1]

client = OmekaClient("http://lbry-web-007.amnh.org/omeka/api", api_key)

response, content = client.get("items", id=22997)


print(response, content)
