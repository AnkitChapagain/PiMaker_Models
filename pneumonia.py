import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

class PneumoniaDetector:
    def __init__(self):
        """Initialize the detector, load the trained model."""
        self.model = tf.keras.models.load_model('pneumonia.h5')
    
    def upload_image(self, image_path):
        """Uploads the image and prepares it for prediction."""
        img = image.load_img(image_path, target_size=(128, 128))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        self.img = img_array / 255.0  # Rescale the image

    def predict(self):
        """Makes a prediction on the uploaded image."""
        prediction = self.model.predict(self.img)
        if prediction[0][0] > 0.5:
            return "No Pneumonia"
        else:
            return "Pneumonia Detected"