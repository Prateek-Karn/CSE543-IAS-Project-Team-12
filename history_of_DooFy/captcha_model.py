import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import os

def load_quickdraw_data(class_name, dataset_path='C:/Users/soumy/OneDrive/Desktop/npy-dataset'):
    file_path = os.path.join(dataset_path, f'{class_name}.npy')
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset for class '{class_name}' not found.")
    
    data = np.load(file_path)
    data = data / 255.0  # Normalize the data
    data = np.resize(data, (data.shape[0], 28, 28, 1))  # Reshape for CNN (samples, 28, 28, 1)
    
    return data

# Load airplane and non-airplane datasets
class_name_airplane = 'airplane'
class_name_not_airplane = 'banana'  # You can choose any other class

quickdraw_data_airplane = load_quickdraw_data(class_name_airplane)
quickdraw_data_not_airplane = load_quickdraw_data(class_name_not_airplane)

# Create labels: 1 for airplane, 0 for non-airplane
labels_airplane = np.ones((quickdraw_data_airplane.shape[0], 1))
labels_not_airplane = np.zeros((quickdraw_data_not_airplane.shape[0], 1))

# Combine datasets and labels
x_data = np.concatenate([quickdraw_data_airplane, quickdraw_data_not_airplane], axis=0)
y_data = np.concatenate([labels_airplane, labels_not_airplane], axis=0)

# Shuffle the data
indices = np.arange(x_data.shape[0])
np.random.shuffle(indices)
x_data = x_data[indices]
y_data = y_data[indices]

# Split into training and validation sets
split_idx = int(0.8 * len(x_data))
x_train, x_val = x_data[:split_idx], x_data[split_idx:]
y_train, y_val = y_data[:split_idx], y_data[split_idx:]

# Define a simple CNN model
def build_model():
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))  # Binary classification output
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Build and train the model
model = build_model()
model.summary()

# Train the model
history = model.fit(x_train, y_train, epochs=10, validation_data=(x_val, y_val))

# Save the trained model
model.save('captcha_model.keras')
