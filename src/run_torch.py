#!/usr/bin/env python3

import subprocess as sp
import sys
import json

image_path = sys.argv[1]
images_dir = "static/data/original"
files_dir = "static/data/files"
items_dir = "static/data/items"

image_map = {}
with open("static/data/name.item") as f:
    for line in f:
        file_name, item_id = line.split()
        image_map[file_name] = int(item_id)
out = sp.getoutput("th src/process.lua  compare pretrained/resnet-34.t7 " + image_path)

# Categories for what it looks like
looks_like = []
for line in out.split("\n")[:5]:
    split = line.strip().split()
    prob = float(split[0])
    cls = " ".join(split[1:])
    looks_like.append((float(prob), cls))

# Separate out similar images and their metadata
similars = []
tags = {}
elements = {}
types = {}
for line in out.split("\n")[6:]:
    dist, img_name = line.strip().split()
    item_id = int(image_map[img_name])
    item_path = "static/data/items/%06i.json" % item_id
    with open(item_path) as f:
        j = json.load(f)

    # Get tags
    for tag in j["tags"]:
        tags[int(tag["id"])] = tag["name"]

    for element in j['element_texts']:
        name = element['element']['name']
        if name not in elements:
            elements[name] = {}
        element_id = int(element['element']['id']) 
        if element_id not in elements[name]:
            elements[name][element_id] = []
        if element['text'] not in elements[name][element_id]:
            elements[name][element_id].append(element['text'])

    types[int(j['item_type']['id'])] = j['item_type']['name']
    similars.append([img_name, dist])

# Print out stuff
print("<table style=\"float: right;\">", end='')
print("<tr><th>ImageNet Category</th><th>Probability</th></tr>", end='')
for item in looks_like:
    print("  <tr><td>%s</td><td>%s%%</td></tr>" % (item[1], item[0]), end='')
print("</table>", end='')

print("<h2>Uploaded Image</h2>", end='')
print("<img style=\"margin-left: 50px;\" src=\"/%s\"><br>" % image_path, end='')


print("<h2>Similar Images</h2>", end='')
for img_name, dist in similars:
    print("<figure><img src=\"/static/data/thumbnails/%s\"><figcaption>Distance: %s <input type=\"checkbox\" name=\"%s\"</figcaption></figure>" % (img_name, dist, img_name), end='')

print("<br><br><h2>Tags</h2><ul>", end='')
for tag_id in tags:
    print('  <li><input type="checkbox" name="%s"/>%s</li>' % (tag_id, tags[tag_id]), end='')
print("</ul>", end='')

print("<h2>Types</h2><ul>", end='')
for type_id in types:
    print('  <li><input type="checkbox" name="%s"/>%s</li>' % (type_id, types[type_id]), end='')
print("</ul>", end='')

print("<h2>Elements</h2><ul>", end='')
for name in sorted(elements):
    for element_id in elements[name]:
        for element in elements[name][element_id]:
            print("  <li><input type=\"checkbox\" name=\"%s\"/> <strong>%s</strong>: %s</li>" %
                  (name, element, element_id), end='')
print("</ul>", end='')

    
