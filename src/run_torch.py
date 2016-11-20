#!/usr/bin/env python3
import subprocess as sp
import sys
import json

image_path = sys.argv[1]
images_dir = "../data/original"
files_dir = "../data/files"
items_dir = "../data/items"

image_map = {}
with open("../data/name.item") as f:
    for line in f:
        file_name, item_id = line.split()
        image_map[file_name] = int(item_id)
    

out = sp.getoutput("th process.lua  compare ../pretrained/resnet-34.t7 " + image_path)

# Categories for what it looks like
looks_like = []
for line in out.split("\n")[:5]:
    split = line.strip().split()
    prob = float(split[0])
    cls = " ".join(split[1:])
    looks_like.append((float(prob), cls))

# Separate out similar images and their metadata
similar = []
tags = {}
elements = {}
types = {}
for line in out.split("\n")[7:]:
    dist, img_name = line.strip().split()
    item_id = int(image_map[img_name])
    item_path = "../data/items/%06i.json" % item_id
    with open(item_path) as f:
        j = json.load(f)

    # Get tags
    for tag in j["tags"]:
        tags[int(tag["id"])] = tag["name"]

    for element in j['element_texts']:
        name = element['element']['name']
        if name not in elements:
            elements[name] = {}
        elements[name][int(element['element']['id'])] = element['text']

    types[int(j['item_type']['id'])] = j['item_type']['name']
    similar.append([img_name, dist])

print("Probable ImageNet categories:")
for item in looks_like:
    print("%5.2f%% %s" % item)

print("\nTAGS: #############################################")
for tag_id in tags:
    print(tags[tag_id])

print("\nTYPES: ############################################")
for type_id in types:
    print(types[type_id])

print("\nELEMENTS: #########################################")
    
for name in sorted(elements):
    for element_id in elements[name]:
        print("%s: %s" % (name, elements[name][element_id]))

    
