

# import numpy as np
import tensorflow as tf
# import tensorflow.python.keras.models as mdl
# from keras.utils.image_utils import img_to_array, load_img

import numpy as np
from tensorflow.python import keras
import cv2

def predict(image):
    img = cv2.imread(image, 0)
    img = cv2.resize(img, (128,128))
    rows, cols= img.shape
    for angle in range(180):
            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle*2, 1)    #Rotate 0 degree
            img_rotated = cv2.warpAffine(img, M, (128, 128))

    # Load a pre-trained Keras model
    model_path = "./content/pretrained_model.h5"
    model = tf.keras.models.load_model(img_rotated)

    model.summary()
    
    sample_input = np.random.rand(1, 128, 128, 1)  # Example input
    predictions = model.predict(sample_input)
    print("Predictions:", predictions)
    return predictions