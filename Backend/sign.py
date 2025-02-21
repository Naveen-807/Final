import cv2
import numpy as np
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from inference_sdk import InferenceHTTPClient
import threading
import queue
import logging
import os
import tempfile
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class SignLanguageRecognizer:
    def __init__(self):
        self.api_key = os.getenv('ROBOFLOW_API_KEY', 'VPR9lg8GcJdrBTP4yd0S')
        self.model_id = "hand-gestures-8frsz/3"
        
        # Initialize client
        self.client = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key=self.api_key
        )
        
        # Video capture variables
        self.video = None
        self.prediction_queue = queue.Queue(maxsize=10)
        self.is_running = False
        self.camera_lock = threading.Lock()
        self.prediction_thread = None

    def start_camera(self):
        """Start the camera and prediction thread"""
        with self.camera_lock:
            if not self.is_running:
                try:
                    self.video = cv2.VideoCapture(0)
                    if not self.video.isOpened():
                        raise Exception("Could not open camera")
                    
                    self.is_running = True
                    self.prediction_thread = threading.Thread(target=self.predict_continuously)
                    self.prediction_thread.daemon = True
                    self.prediction_thread.start()
                    return True
                except Exception as e:
                    logger.error(f"Failed to start camera: {e}")
                    self.stop_camera()
                    return False
            return False

    def stop_camera(self):
        """Stop the camera and prediction thread"""
        with self.camera_lock:
            self.is_running = False
            if self.video is not None:
                self.video.release()
                self.video = None
            # Clear the prediction queue
            while not self.prediction_queue.empty():
                try:
                    self.prediction_queue.get_nowait()
                except queue.Empty:
                    break
            return True

    def predict_continuously(self):
        """Continuously predict sign language gestures in background thread"""
        while self.is_running:
            try:
                if self.video is None or not self.video.isOpened():
                    break

                ret, frame = self.video.read()
                if not ret:
                    continue

                # Create temporary file for the frame
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                    cv2.imwrite(temp_file.name, frame)
                    
                    # Run inference
                    predictions = self.client.infer(
                        temp_file.name, 
                        model_id=self.model_id
                    )
                
                # Remove temporary file
                os.unlink(temp_file.name)

                # Annotate frame with predictions
                annotated_frame = self.annotate_frame(frame, predictions)

                # Update prediction queue
                if self.prediction_queue.full():
                    self.prediction_queue.get()
                self.prediction_queue.put({
                    'frame': annotated_frame,
                    'predictions': predictions,
                    'timestamp': datetime.utcnow().isoformat()
                })

            except Exception as e:
                logger.error(f"Prediction error: {e}")
                continue

    def annotate_frame(self, frame, predictions):
        """Annotate frame with bounding boxes and labels"""
        if 'predictions' in predictions:
            for prediction in predictions['predictions']:
                x = int(prediction['x'])
                y = int(prediction['y'])
                width = int(prediction['width'])
                height = int(prediction['height'])
                
                # Draw bounding box
                cv2.rectangle(
                    frame, 
                    (x - width//2, y - height//2), 
                    (x + width//2, y + height//2), 
                    (0, 255, 0), 
                    2
                )

                # Add gesture label
                label = f"{prediction['class']}: {prediction['confidence']:.2f}"
                cv2.putText(
                    frame, 
                    label, 
                    (x - width//2, y - height//2 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.9, 
                    (0, 255, 0), 
                    2
                )
        
        return frame

    def get_frame_with_predictions(self):
        """Get the latest frame with predictions"""
        if not self.is_running:
            return None, None

        try:
            if not self.prediction_queue.empty():
                data = self.prediction_queue.get()
                frame = data['frame']
                predictions = data['predictions']

                # Encode frame
                ret, jpeg = cv2.imencode('.jpg', frame)
                return jpeg.tobytes(), predictions
        except Exception as e:
            logger.error(f"Error getting frame: {e}")
        
        return None, None

# Initialize global recognizer
recognizer = SignLanguageRecognizer()

@app.route('/camera/start', methods=['POST'])
def start_camera():
    """Start the camera"""
    success = recognizer.start_camera()
    return jsonify({'success': success})

@app.route('/camera/stop', methods=['POST'])
def stop_camera():
    """Stop the camera"""
    success = recognizer.stop_camera()
    return jsonify({'success': success})

@app.route('/camera/status')
def camera_status():
    """Get camera status"""
    return jsonify({
        'is_running': recognizer.is_running,
        'has_camera': recognizer.video is not None and recognizer.video.isOpened()
    })

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    def generate():
        while True:
            frame, _ = recognizer.get_frame_with_predictions()
            if frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    return Response(generate(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/current_gesture')
def current_gesture():
    """Get current sign language gesture"""
    _, predictions = recognizer.get_frame_with_predictions()
    
    if predictions and 'predictions' in predictions and len(predictions['predictions']) > 0:
        top_prediction = max(
            predictions['predictions'], 
            key=lambda x: x['confidence']
        )
        return jsonify({
            'gesture': top_prediction['class'],
            'confidence': top_prediction['confidence']
        })
    
    return jsonify({
        'gesture': 'No gesture detected',
        'confidence': 0
    })

@app.route('/supported_gestures')
def supported_gestures():
    """List of supported sign language gestures"""
    return jsonify({
        'gestures': [
            {
                'name': 'Thumbs Up',
                'description': 'A positive or affirmative gesture',
                'meaning': 'Yes/Good'
            },
            {
                'name': 'Peace',
                'description': 'V sign with index and middle finger',
                'meaning': 'Peace/Victory'
            },
            {
                'name': 'Open Hand',
                'description': 'Palm facing forward with spread fingers',
                'meaning': 'Stop/Hello'
            },
            {
                'name': 'Closed Fist',
                'description': 'Closed hand gesture',
                'meaning': 'Zero/Hold'
            },
            {
                'name': 'Rock On',
                'description': 'Extended index and pinky fingers',
                'meaning': 'I love you (in ASL)'
            }
        ]
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)