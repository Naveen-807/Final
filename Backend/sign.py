import os
import cv2
import numpy as np
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from inference_sdk import InferenceHTTPClient
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Roboflow Configuration
ROBOFLOW_API_KEY = "VPR9lg8GcJdrBTP4yd0S"
ROBOFLOW_MODEL_ID = "hand-gestures-8frsz/3"

class HandGestureDetector:
    def __init__(self, api_key, model_id):
        self.client = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key=api_key
        )
        self.model_id = model_id

    def detect_gesture(self, image_path):
        try:
            # Perform inference
            result = self.client.infer(
                image_path, 
                model_id=self.model_id
            )
            
            # Process and return detections
            return self._parse_detections(result)
        
        except Exception as e:
            print(f"Gesture detection error: {e}")
            return []
    
    def _parse_detections(self, result):
        detections = []
        
        if 'predictions' in result:
            for pred in result['predictions']:
                detection = {
                    'class': pred.get('class', 'Unknown'),
                    'confidence': pred.get('confidence', 0),
                    'bbox': {
                        'x': pred.get('x', 0),
                        'y': pred.get('y', 0),
                        'width': pred.get('width', 0),
                        'height': pred.get('height', 0)
                    }
                }
                detections.append(detection)
        
        return detections

    def visualize_detections(self, image_path, detections):
        # Load image
        image = cv2.imread(image_path)
        
        # Draw bounding boxes
        for detection in detections:
            x = int(detection['bbox']['x'] - detection['bbox']['width'] / 2)
            y = int(detection['bbox']['y'] - detection['bbox']['height'] / 2)
            w = int(detection['bbox']['width'])
            h = int(detection['bbox']['height'])
            
            # Draw rectangle
            cv2.rectangle(
                image, 
                (x, y), 
                (x + w, y + h), 
                (0, 255, 0), 
                2
            )
            
            # Add label
            label = f"{detection['class']}: {detection['confidence']:.2f}"
            cv2.putText(
                image, 
                label, 
                (x, y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.9, 
                (0, 255, 0), 
                2
            )
        
        # Save annotated image
        output_path = 'detected_gestures.jpg'
        cv2.imwrite(output_path, image)
        return output_path

def base64_to_image(base64_string):
    """
    Convert base64 string to image file
    """
    try:
        # Remove header if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decode base64
        image_bytes = base64.b64decode(base64_string)
        
        # Convert to numpy array
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        
        # Decode image
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        # Save temporary image
        temp_image_path = 'temp_uploaded_image.jpg'
        cv2.imwrite(temp_image_path, image)
        
        return temp_image_path
    
    except Exception as e:
        print(f"Image conversion error: {e}")
        return None

# Initialize Gesture Detector
gesture_detector = HandGestureDetector(
    api_key=ROBOFLOW_API_KEY, 
    model_id=ROBOFLOW_MODEL_ID
)

@app.route('/detect_gesture', methods=['POST'])
def detect_gesture():
    try:
        # Get base64 image from request
        data = request.get_json()
        base64_image = data.get('image')
        
        # Validate input
        if not base64_image:
            return jsonify({
                'success': False, 
                'message': 'No image provided'
            }), 400
        
        # Convert base64 to image file
        image_path = base64_to_image(base64_image)
        
        # Validate image conversion
        if not image_path:
            return jsonify({
                'success': False, 
                'message': 'Invalid image format'
            }), 400
        
        # Perform gesture detection
        detections = gesture_detector.detect_gesture(image_path)
        
        # Optional: Visualize detections
        if detections:
            visualization_path = gesture_detector.visualize_detections(image_path, detections)
        
        # Prepare response
        response = {
            'success': True,
            'detections': detections,
            'visualization_path': visualization_path if detections else None
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Detection error: {e}")
        return jsonify({
            'success': False, 
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Sign Language Detection Backend is running'
    })

def setup_environment():
    """
    Ensure necessary directories and configurations
    """
    # Create directories if they don't exist
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('detections', exist_ok=True)

if __name__ == '__main__':
    # Setup environment
    setup_environment()
    
    # Run Flask app
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=True
    )