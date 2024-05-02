import torch
import torch.nn as nn
import torchvision
from torchvision import models, transforms
from PIL import Image
device = "cuda" if torch.cuda.is_available() else "cpu"
parameter = torch.load("best_model.pth", map_location=device)

model = torchvision.models.efficientnet_b4(pretrained=True)

model.classifier = nn.Sequential(
    nn.Dropout(p=0.3, inplace=True),
    nn.Linear(model.classifier[1].in_features, 5)
    )

model.load_state_dict(parameter)

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) 
])

image_path = "img.jpg"
image = Image.open(image_path)

input_tensor = preprocess(image)
input_batch = input_tensor.unsqueeze(0) 

model.eval()

with torch.no_grad():
    output = model(input_batch)

probabilities = torch.nn.functional.softmax(output[0], dim=0)

top_prob, top_catid = torch.topk(probabilities, 1)
print('(Heart: 0, Oblong: 1, Oval: 2, Round: 3, Square: 4)')
print('top_prob : ',top_prob[0])
print('top_catid : ',top_catid[0])

# https://www.kaggle.com/code/baranbingl/face-shape-detection-85-acc-on-test-set/notebook