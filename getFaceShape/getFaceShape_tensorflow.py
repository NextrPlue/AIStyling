
from keras.applications.vgg16 import preprocess_input
from keras.models import load_model
from PIL import Image
import numpy as np

img_path = 'img.jpg'

img = Image.open(img_path).resize((224,224))
arr = np.asarray(img)
arr = np.expand_dims(arr, axis=0)
x = preprocess_input(arr)

model = load_model('new_face_classifier.h5')

result = model.predict(x)
print('Heart : 1, Oblong : 2, Oval : 3, Round : 4, Square : 5')
print(result[0].max())
print(result[0].argmax() + 1)

#https://www.kaggle.com/code/bradwel/facial-classification-model/output?select=new_face_classifier.h5