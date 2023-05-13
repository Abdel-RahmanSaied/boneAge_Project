import tensorflow as tf
from tensorflow import keras
# from keras.preprocessing.image import img_to_array, load_img
import numpy as np

# Load the model
model = keras.models.load_model('ml_model/bone_age_weights.bes.hdf5')
print("xxxxxxxxxxx")
# Define the path to the image you want to predict on
image_path = "path/to/image.jpg"

# Load and preprocess the image
img = load_img(image_path, target_size=(256, 256))
img = img_to_array(img) / 255.
img = np.expand_dims(img, axis=0)

# Make a prediction on the image
age = model.predict(img)[0][0]

# Print the predicted age
print("Predicted age:", age)