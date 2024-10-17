import cv2
import tensorflow as tf
import numpy as np
import requests
import os
import threading
import queue
import time
from keras.preprocessing.image import ImageDataGenerator

# reading data that is required to be trained on
train_data = "../FYP/Fire Dataset/Fire-Detection"
print(os.listdir(train_data))

# Using tensorflow's ImageDataGenerator to prepare the image-data for training
train_gen = ImageDataGenerator(width_shift_range = 0.5,
                               height_shift_range = 0.5,
                               validation_split = 0.2)

train_set = train_gen.flow_from_directory(train_data,target_size = (300,300),class_mode = 'binary',subset = 'training',batch_size = 8)

validation_set = train_gen.flow_from_directory(train_data,target_size = (300,300),class_mode = 'binary',subset = 'validation',batch_size = 8)

# Loading the model
best_model = tf.keras.models.load_model('/final_model_FIRE.h5')
best_model.evaluate(validation_set)

# Function to send an alert
def send_alert(event_type):
    url = 'http://192.168.100.47:5000/alert'
    data = {"event": event_type}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Alert sent successfully")
    else:
        print("Failed to send alert")


# Function to apply preprocessing to reduce the effect of lighting
def preprocess_frame(frame, img_shape=300):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply adaptive histogram equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Edge detection using Canny
    edges = cv2.Canny(gray, 100, 200)

    # Convert edges to 3 channels
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Resize the image
    edges = cv2.resize(edges, (img_shape, img_shape))

    return edges


# Function to read image and give desired output with image
def pred_and_plot(model, frame, class_names):
    """
    Imports an image located at filename, makes a prediction on it with
    a trained model and plots the image with the predicted class as the title.
    """
    # Preprocess the frame
    img = preprocess_frame(frame)

    # Make a prediction
    pred = model.predict(tf.expand_dims(img, axis=0))

    if len(pred[0]) > 0.8:  # Check for multi-class
        pred_class = class_names[pred.argmax()]  # If more than one output, take the max
    else:
        pred_class = class_names[int(tf.round(pred)[0][0])]  # If only one output, round

    # Send alert if fire is detected
    if pred_class == "Fire":
        send_alert("FIRE")

    return pred_class


# Predefining class names
class_names = ['Not-fire', 'Fire']


# Function to read frames from the camera in a separate thread
def camera_reader_thread(url, frame_queue):
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Warning: Lost connection to the camera.")
            break

        # Put the frame in the queue
        if not frame_queue.full():
            frame_queue.put(frame)
        time.sleep(0.01)  # Slight delay to reduce CPU usage

    cap.release()


# Function to process frames from the queue
def process_frames(frame_queue, model, class_names):
    # Initial window size
    window_width = 640
    window_height = 480
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Video', window_width, window_height)

    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()

            # Resize the frame to the desired window size
            frame = cv2.resize(frame, (window_width, window_height))

            # Process the frame (preprocess and predict)
            pred_class = pred_and_plot(model, frame, class_names)

            # Display the resulting frame with prediction
            cv2.putText(frame, f"Prediction: {pred_class}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Video', frame)

            # Check for user input to adjust window size
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('+'):
                window_width += 20
                window_height += 15
                cv2.resizeWindow('Video', window_width, window_height)
            elif key == ord('-'):
                window_width = max(200, window_width - 20)
                window_height = max(150, window_height - 15)
                cv2.resizeWindow('Video', window_width, window_height)

    cv2.destroyAllWindows()


# Main function to start the camera reader thread and frame processor
def main():
    rtsp_url = "rtsp://admin:Nandaasad_@192.168.100.30/stream"
    frame_queue = queue.Queue(maxsize=10)

    # Start the camera reader thread
    threading.Thread(target=camera_reader_thread, args=(rtsp_url, frame_queue), daemon=True).start()

    # Start processing frames
    process_frames(frame_queue, best_model, class_names)


if __name__ == "__main__":
    main()
