#!/usr/bin/env th

require("image")
require("cunn")
require("cudnn")
require("optim")
require("paths")

-- From facebook's code
local transforms = require('src/transforms')
local imagenet = require('src/imagenet')
local meanstd = { mean = { 0.485, 0.456, 0.406 },
                  std = { 0.229, 0.224, 0.225 }, }
local transform = transforms.Compose{ transforms.Scale(256),
                                      transforms.ColorNormalize(meanstd),
                                      transforms.CenterCrop(224), }

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
  
  -- Load image and model
  local img = load_image(image_path)
  local prepared_img = prepare_image(img)

  -- Process class
  local output = model:forward(prepared_img):squeeze()

  -- Save the image if there's only one
  if total == 1 then 
    local probs, indexes = output:topk(n_classes, true, true)
    local classes = {}
    for n = 1, n_classes do
      print(string.format("%6.2f %s", 100 * probs[n], imagenet[indexes[n]]))
    end
    print("")

    -- image.save(string.format("%s_crop.jpg", basename), prepared_img[1]:float())
  else
    print(string.format("%6.2f %-32s", 100 * position / total, basename))
  end

  -- Calculate
  return model.modules[10].output:float()
end

function main()
  -- Process arguments
  local command = arg[1]
  local model_path = arg[2]
  local model = load_model(model_path)
  local n_classes = 5

  -- If there are multiple arguments then just process those
  if command == "image" then
    local basenames = {}
    local features = torch.FloatTensor(#arg - 2, 512)
    for i, image_path in ipairs(arg) do
      if i > 2 then
        basenames[i - 2] = paths.basename(image_path)
        features[{{i - 2}, {}}] = process(model, image_path, n_classes, i - 2, #arg - 2)
      end
    end
    torch.save("args.t7", {basenames, features})
  end

  -- otherwise process original
  if command == "original" then 
    require("src/original")
    local basenames = {}
    local features = torch.FloatTensor(#original, 512)
    for i, image_path in ipairs(original) do
      basenames[i] = paths.basename(image_path)
      features[{{i}, {}}] = process(model, image_path, n_classes, i, #original)
    end
    torch.save("src/original.t7", {basenames, features})
  end

  -- If we're comparing against older then do so
  if command == "compare" then
    local image_path = arg[3]
    local tab = torch.load("src/original.t7")
    local basenames = tab[1]
    local features = tab[2]
    local feature = process(model, image_path, n_classes, 1, 1):cuda()
    local distances = (features:cuda() - feature:expandAs(features)):pow(2):sum(2):sqrt()

    -- Print 5 closest
    n_classes = 12
    local dists, indexes = distances:view(distances:size(1)):topk(n_classes, false, true)
    for n = 1, n_classes do
      local index = indexes[n]
      print(string.format("%6.2f %s", distances[index][1], basenames[index]))
    end 
  end
end


main()
