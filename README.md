# ImageArtifcats

Presentation: https://docs.google.com/presentation/d/1kuj-l0sENOyYHcobQ6fzM0OtamjIBFHsZnV6shHZh_g/edit?usp=sharing

pretrained/resnet-34.t7: your t7 torch resnet model should go here
server.py: file to run with flask
src/get_jsons.py:  our REST wrapper to download all all items (metadata) and files (image links) you will need to create folders for each in static/
src/get_omeka_images.py: download images from links provided from OMEKA rest
src/imagenet.lua: code from FAIR that prepares images for their models
src/key: you will need to put your OMEKA API key here
src/omekaclient.py: Omeka's provided client that we upgraded to python3
src/original.lua: table of each picture in lua for easy injestion
src/original.t7: list of feature vector and basename for each image
src/process.lua: run the neural network through commands (image|original|compare)
src/run_torch.py: generates the output list of images, classifications, and metadata in html
src/transforms.lua: code from FAIR that prepares images for their models
static/style.css: style for all pages
static/arifcats_logo.png: main page picture
static/arifcats_derp.png: thanks page picture
static/images/: store uploaded images here
templates/upload.html: template for upload (main) page
templates/classify.html: template for classify page that displays results and metadata
templates/thanks.html: template for final page
