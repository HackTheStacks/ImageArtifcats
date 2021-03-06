#!/usr/bin/python3

import os
import sys
from omekaclient import OmekaClient
import json

def main():
    # Get Key
    with open('key') as f:
        api_key = f.readline()[:-1]

        
    # Get destination
    dest = sys.argv[1]
    element = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    if not os.path.exists(dest):
        print("Destination does not exist!")
        sys.exit(1)

    # Connect to database
    client = OmekaClient("http://lbry-web-007.amnh.org/digital/api", api_key)

    # Go through each item
    fail = []
    for i in range(start, end):
        response, content = client.get(element, id=i)
        j = json.loads(content.decode("utf-8"))
        if response.status == 200:
            print("Writing %6i " % i)
            filename = "%s/%s/%06i.json" % (dest, element, i)
            with open(filename, 'w') as f:
                f.write(json.dumps(j, sort_keys=True, indent=2))
        else:
            print("FAIL! %6i |%s|" % (i, response.status))
    
if __name__ == "__main__":
    main()
