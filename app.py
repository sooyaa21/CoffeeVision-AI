import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from predict import predict_image

app = Flask(__name__)

# ==========================
# Configuration
# ==========================

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================
# Helper Function
# ==========================

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ==========================
# Home
# ==========================

@app.route("/")
def home():
    return render_template("dashboard.html")


# ==========================
# Prediction
# ==========================

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return render_template(
            "dashboard.html",
            error="Please upload an image first."
        )

    file = request.files["image"]

    if file.filename == "":
        return render_template(
            "dashboard.html",
            error="No image selected."
        )

    if not allowed_file(file.filename):
        return render_template(
            "dashboard.html",
            error="Only JPG, JPEG, and PNG files are allowed."
        )

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    prediction, confidence, probabilities = predict_image(filepath)

    return render_template(
        "dashboard.html",
        image=filepath,
        prediction=prediction,
        confidence=round(confidence, 2),
        probabilities=probabilities
    )


# ==========================
# Run App
# ==========================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )