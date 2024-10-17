import cv2
import numpy as np
from keras.models import load_model
import requests
from collections import deque
import threading
import time
import os


def send_alert(event_type):
    url = 'http://192.168.100.47:5000/alert'
    data = {"event": event_type}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Alert sent successfully")
        else:
            print(f"Alert failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


class CameraProcessor:
    def __init__(self, camera_url):
        self.camera_url = camera_url
        self.frame_buffer = deque(maxlen=1)
        self.capture_thread = threading.Thread(target=self.capture_frames)
        self.process_thread = threading.Thread(target=self.process_frames)
        self.running = True
        self.model = load_model('./model.h5')
        self.Q = deque(maxlen=128)

    def start(self):
        self.capture_thread.start()
        self.process_thread.start()

    def stop(self):
        self.running = False
        self.capture_thread.join()
        self.process_thread.join()

    def capture_frames(self):
        vs = cv2.VideoCapture(self.camera_url)
        if not vs.isOpened():
            print("Error: Could not open video stream.")
            return

        while self.running:
            grabbed, frame = vs.read()
            if not grabbed:
                print("Frame not grabbed. Retrying...")
                time.sleep(0.1)
                continue
            self.frame_buffer.append(frame)
        vs.release()

    def process_frames(self):
        writer = None
        window_name = "Frame"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        window_width, window_height = 800, 600
        cv2.resizeWindow(window_name, window_width, window_height)

        frame_count = 0
        while self.running:
            if not self.frame_buffer:
                time.sleep(0.01)
                continue
            frame = self.frame_buffer.pop()

            # Convert to RGB and preprocess for the model
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (128, 128)).astype("float16")
            frame_normalized = frame_resized / 255.0

            # Model prediction
            preds = self.model.predict(np.expand_dims(frame_normalized, axis=0))[0]
            self.Q.append(preds)
            results = np.array(self.Q).mean(axis=0)
            label = (results > 0.6)[0]

            # Alert and visualization
            text = "Violence: {}".format(label)
            color = (0, 255, 0)
            if label:
                color = (255, 0, 0)
                send_alert("VIOLENCE")

            cv2.putText(frame_rgb, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
            cv2.imshow(window_name, frame_rgb)

            if writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter("output.mp4", fourcc, 30, (frame.shape[1], frame.shape[0]), True)

            writer.write(cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR))

            frame_count += 1
            print(f"Processed frame count: {frame_count}")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting on user request.")
                break

        if writer is not None:
            writer.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    camera_url = "rtsp://admin:Nandaasad_@192.168.100.30/stream"
    processor = CameraProcessor(camera_url)
    processor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
        processor.stop()
