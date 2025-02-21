# filepath: /workspaces/Ctrl-alt/sign.py
import cv2
import mediapipe as mp
import tensorflow as tf
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Load the pre-trained model
model = tf.keras.models.load_model('path/to/your/pretrained/model.h5')

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Define a function to recognize gestures using the pre-trained model
def recognize_gesture(landmarks):
    # Extract the coordinates of the landmarks
    coords = np.array([[landmark.x, landmark.y, landmark.z] for landmark in landmarks]).flatten()
    # Predict the gesture using the pre-trained model
    prediction = model.predict(np.expand_dims(coords, axis=0))
    gesture = np.argmax(prediction)
    return gesture

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = recognize_gesture(hand_landmarks.landmark)
            cv2.putText(frame, str(gesture), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Sign Language Recognition', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()