import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
import sign_language_translator as slt

class SignLanguageSystem:
    def __init__(self):
        # Initialize MediaPipe hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Load pre-trained CNN model
        self.model = load_model('sign_language_model.h5')
        
        # Initialize SLT for text-to-sign
        self.slt_model = slt.models.ConcatenativeSynthesis(
            text_language="english",
            sign_language="asl",
            sign_format="video"
        )
    
    def detect_sign(self, frame):
        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            # Extract hand landmarks
            landmarks = results.multi_hand_landmarks[0].landmark
            
            # Convert to numpy array
            hand_data = np.array([[l.x, l.y, l.z] for l in landmarks])
            
            # Predict sign
            prediction = self.model.predict(hand_data.reshape(1, 21, 3))
            
            return prediction.argmax()
        
        return None
    
    def text_to_sign(self, text):
        return self.slt_model.translate(text)
    
    def process_video(self, video_path=None):
        if video_path:
            cap = cv2.VideoCapture(video_path)
        else:
            cap = cv2.VideoCapture(0)
            
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
                
            # Detect sign
            sign = self.detect_sign(frame)
            
            # Display results
            if sign is not None:
                cv2.putText(frame, f"Detected Sign: {sign}", 
                           (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                           1, (0, 255, 0), 2)
            
            cv2.imshow('Sign Language Detection', frame)
            
            if cv2.waitKey(5) & 0xFF == 27:
                break
                
        cap.release()
        cv2.destroyAllWindows()