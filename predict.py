import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# ==========================
# Load Model
# ==========================

MODEL_PATH = "model/coffee_model.keras"
CLASS_PATH = "model/class_names.txt"

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_PATH, "r") as file:
    class_names = [line.strip() for line in file.readlines()]


# ==========================
# Prediction Function
# ==========================

def predict_image(img_path):

    # Load Image
    img = image.load_img(
        img_path,
        target_size=(224, 224)
    )

    # Convert Image
    img = image.img_to_array(img)
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)

    # Predict
    prediction = model.predict(
        img,
        verbose=0
    )[0]

    # Best Result
    class_index = np.argmax(prediction)

    predicted_class = class_names[class_index]

    confidence = round(
        float(prediction[class_index]) * 100,
        2
    )

    return (
        predicted_class,
        confidence,
        prediction.tolist()
    )