import os
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# ===========================
# PATH DATASET
# ===========================

train_dir = "dataset/train"
test_dir = "dataset/test"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10

# ===========================
# IMAGE GENERATOR
# ===========================

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

test_datagen = ImageDataGenerator(
    rescale=1./255
)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

validation_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    shuffle=False
)

# ===========================
# MOBILENETV2
# ===========================

base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224,224,3)
)

base_model.trainable = False

# ===========================
# MODEL
# ===========================

model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dropout(0.3),
    Dense(128, activation="relu"),
    Dropout(0.3),
    Dense(4, activation="softmax")
])

model.summary()

# ===========================
# COMPILE
# ===========================

model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ===========================
# TRAINING
# ===========================

history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=EPOCHS
)

# ===========================
# EVALUASI
# ===========================

loss, accuracy = model.evaluate(test_generator)

print(f"\nTest Accuracy : {accuracy*100:.2f}%")
print(f"Test Loss     : {loss:.4f}")

# ===========================
# SIMPAN MODEL
# ===========================

os.makedirs("model", exist_ok=True)

model.save("model/coffee_model.keras")

print("\nModel berhasil disimpan!")

# ===========================
# SIMPAN NAMA KELAS
# ===========================

class_names = list(train_generator.class_indices.keys())

with open("model/class_names.txt", "w") as f:
    for item in class_names:
        f.write(item + "\n")

print("Class names berhasil disimpan!")

# ===========================
# GRAFIK ACCURACY
# ===========================

plt.figure(figsize=(10,5))

plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")

plt.title("Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

plt.show()

# ===========================
# GRAFIK LOSS
# ===========================

plt.figure(figsize=(10,5))

plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")

plt.title("Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

plt.show()