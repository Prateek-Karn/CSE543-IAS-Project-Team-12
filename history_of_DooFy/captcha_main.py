import numpy as np
from tensorflow.keras.models import load_model
from drawing_app import DrawingApp  # Import the Tkinter drawing app

# Load the pre-trained CNN model
model = load_model('captcha_model.keras')  # Ensure the path is correct

def preprocess_image(user_image):
    """ Preprocess the user's drawing to be passed to the model """
    # Reshape for the CNN model: (28, 28) -> (1, 28, 28, 1)
    user_image = user_image.reshape(1, 28, 28, 1)
    return user_image

def compare_drawings(user_image):
    """ Use the CNN model to predict if the drawing is correct """
    preprocessed_image = preprocess_image(user_image)
    prediction = model.predict(preprocessed_image)
    
    # Extract the prediction value from the array
    prediction_value = prediction[0][0]
    
    # If the model predicts > 0.5, it's considered a match
    threshold = 1
    if prediction_value >= threshold:
        return True
    return False

def on_submit(app):
    user_image = app.get_image_data()
    is_match = compare_drawings(user_image)
    
    if is_match:
        print("CAPTCHA passed!")
    else:
        print("CAPTCHA failed. Try again.")

if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    app = DrawingApp(root)

    submit_button = tk.Button(root, text="Submit", command=lambda: on_submit(app))
    submit_button.pack()

    root.mainloop()
