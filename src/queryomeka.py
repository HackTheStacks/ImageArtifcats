#!/usr/bin/python3

import sys
from omekaclient import OmekaClient
import json
with open('key') as f:
    api_key = f.readline()[:-1]

client = OmekaClient("http://lbry-web-007.amnh.org/digital/api", api_key)

if sys.argv[1] == 'resources':
    response, content = client.get("resources")
    j = json.loads(content.decode("utf-8"))
    print(json.dumps(j, sort_keys=True, indent=2))
elif sys.argv[1] == 'files':
    response, content = client.index("files")
    j = json.loads(content.decode("utf-8"))
    print(json.dumps(j, sort_keys=True, indent=2))

