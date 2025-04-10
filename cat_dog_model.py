import tensorflow as tf
import numpy as np
import cv2

class PIMakerCatDog:
    def __init__(self):
        """Initialize without loading the model or camera immediately."""
        self.model = None
        self.cap = None

    def loadmodel(self, model_path):
        """Load the model safely."""
        try:
            self.model = tf.keras.models.load_model(model_path)
            print(f"✅ Model loaded from {model_path}")
            return self.model
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return None

    def opencamera(self):
        """Open the webcam and return the capture object."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("❌ Error: Could not open webcam.")
            return None
        return self.cap

    def didcameraopen(self, camera):
        """Check if the camera opened successfully."""
        if camera is None or not camera.isOpened():
            print("❌ Error: Camera is not working.")
            return False
        return True

    def read(self, camera):
        """Capture a frame from the camera."""
        ret, frame = camera.read()
        if not ret:
            print("❌ Error: Failed to capture frame.")
            return None, None
        return ret, frame

    def preprocess_frame(self, frame):
        """Resize and normalize the frame for model prediction."""
        if self.model is None:
            print("❌ Error: No model loaded.")
            return None

        try:
            # Get expected input shape
            expected_shape = self.model.input_shape  # Example: (None, 256, 256, 3)
            print(f"📏 Model expects input shape: {expected_shape}")

            # Resize and normalize
            frame = cv2.resize(frame, (256, 256))  
            frame = frame / 255.0  

            # Expand dimensions
            frame = np.expand_dims(frame, axis=0)  

            return frame
        except Exception as e:
            print(f"❌ Error preprocessing frame: {e}")
            return None

    def predicted(self, frame, model):
        """Predict whether the image is a cat or dog."""
        processed_frame = self.preprocess_frame(frame)
        if processed_frame is None:
            return None
        
        try:
            prediction = model.predict(processed_frame)
            return prediction
        except Exception as e:
            print(f"❌ Error during prediction: {e}")
            return None

    def output(self, frame, prediction):
        """Display the prediction on the webcam frame."""
        if prediction is None:
            return

        class_label = "🐶 Dog" if prediction[0][0] > 0.5 else "🐱 Cat"
        cv2.putText(frame, f"Prediction: {class_label}", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Cat vs Dog Detection", frame)

    def exits(self):
        """Check if 'q' is pressed to exit."""
        return cv2.waitKey(1) & 0xFF == ord('q')

    def close(self, camera):
        """Close the webcam and release resources."""
        if camera is not None:
            camera.release()
        cv2.destroyAllWindows()
