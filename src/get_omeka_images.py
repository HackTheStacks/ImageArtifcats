#!/usr/bin/python3

import os
import sys
import json
import urllib.request

def main():
    src = sys.argv[1]
    src_json = os.path.join(src, 'files')
    dst_image = os.path.join(src, 'thumbnails')
    
    # Print filenames
    filenames = sorted(os.listdir(src_json))
    for i, filename in enumerate(filenames):
        path = os.path.join(src_json, filename)
        with open(path) as f:
            j = json.load(f)
        original_url = j['file_urls']['thumbnail']
        image_name = os.path.basename(original_url)
        dst = os.path.join(dst_image, image_name)
        with open(dst, 'wb') as f:
            f.write(urllib.request.urlopen(original_url).read())
        print("%-64s %7.3f%%" % (image_name, 100.0 * i / len(filenames)))
    
if __name__ == "__main__":
    main()
