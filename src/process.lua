#!/usr/bin/env th

require("image")
require("cunn")
require("cudnn")
require("optim")
require("paths")

-- From facebook's code
local transforms = require('transforms')
local imagenet = require('imagenet')
local meanstd = { mean = { 0.485, 0.456, 0.406 },
                  std = { 0.229, 0.224, 0.225 }, }
local transformT = transforms.Compose{ transforms.Scale(256),
                                      transforms.ColorNormalize(meanstd),
                                      transforms.TenCrop(224), }

function load_model(model_path)
  local model = torch.load(model_path)
  model:add(cudnn:SoftMax())
  model:evaluate()
  return model:cuda()
end

function load_image(image_path)
  local img = image.load(image_path)
  if img:size(1) == 1 then
    local img_tmp = torch.FloatTensor(3, img:size(2), img:size(3))
    for i = 1, 3 do 
      img_tmp[{{i}, {}, {}}] = img
    end
    img = img_tmp
  end
  return img
end

function prepare_image(img)
  img = transform(img)
  if img:size():size() == 4 then
    return img:cuda()
  else
    return img:view(1, table.unpack(img:size():totable())):cuda()
  end
end

function process(model, image_path, n_classes, position, total)
  local basename = paths.basename(image_path, '.jpg')
  print(string.format("%-32s %7.3f", basename, 100 * position / total))
  
  -- Load image and model
  local img = load_image(image_path)
  local prepared_img = prepare_image(img)
  -- image.save("../" .. basename .. "_crop.jpg", prepared_img[1])

  -- Process class
  local output = model:forward(prepared_img):squeeze()
  local classes =  {}
  local counts =  {}
  for cut = 1, 10 do 
    local probs, indexes = output[cut]:topk(n_classes, true, true)
    for n = 1, n_classes do
      local class = imagenet[indexes[n]]
      classes[class] = (classes[class] or 0) + probs[n]
      counts[class] = (counts[class] or 0) + 1
    end
  end
  
  -- Print average classes
  for class, prob in pairs(classes) do
    classes[class] = prob / counts[class]
  end

  local features = model.modules[10].output:float()
  torch.save("../features/" .. basename .. ".t7", {classes, features})
end

function main()
  -- Process arguments
  local command = arg[1]
  local model_path = arg[2]
  local model = load_model(model_path)
  local n_classes = 5

  -- If there are multiple arguments then just process those
  if command == "image" then
    for i, image_path in ipairs(arg) do
      if i > 2 then
        process(model, image_path, n_classes, i - 2, #arg - 2)
      end
    end
  end

  -- otherwise process original
  if command == "original" then 
    require("original")
    for i, image_path in ipairs(original) do
      process(model, image_path, n_classes, i, #original)
    end
  end

  -- If we're comparing against older then do so
  if command == "comapre" then
    -- require("existing")
  end
end


main()
