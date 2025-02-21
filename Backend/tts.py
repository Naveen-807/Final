import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import azure.cognitiveservices.speech as speechsdk
import tempfile
import pdfplumber
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get Azure credentials from environment variables
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "centralindia")

# Configure upload folder
UPLOAD_FOLDER = 'temp_uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Available voices
AVAILABLE_VOICES = {
    "en-US-Male": "en-US-GuyNeural",
    "en-US-Female": "en-US-JennyNeural",
    "en-IN-Male": "en-IN-AaravNeural",
    "en-IN-Female": "en-IN-NeerjaNeural",
    "en-GB-Male": "en-GB-RyanNeural",
    "en-GB-Female": "en-GB-SoniaNeural"
}

@app.route('/api/voices', methods=['GET'])
def get_voices():
    return jsonify(list(AVAILABLE_VOICES.keys()))

@app.route('/api/synthesize-text', methods=['POST'])
def synthesize_text():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    text = data['text']
    voice_name = AVAILABLE_VOICES.get(data.get('voice', 'en-US-Male'))
    
    # Configure speech service
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
    speech_config.speech_synthesis_voice_name = voice_name
    
    # Generate unique file name
    file_id = str(uuid.uuid4())
    temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}.wav")
    
    # Configure audio output
    audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_file_path)
    
    # Create synthesizer and generate speech
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()
    
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return jsonify({
            "status": "success",
            "message": "Speech synthesis completed",
            "audioUrl": f"/api/audio/{file_id}"
        })
    else:
        error_details = result.cancellation_details.error_details if result.cancellation_details else "Unknown error"
        return jsonify({"error": f"Speech synthesis failed: {error_details}"}), 500

@app.route('/api/process-pdf', methods=['POST'])
def process_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    pdf_file = request.files['file']
    voice = request.form.get('voice', 'en-US-Male')
    
    if pdf_file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not pdf_file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(pdf_file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        pdf_file.save(pdf_path)
        
        # Extract text from PDF
        with pdfplumber.open(pdf_path) as pdf:
            pdf_text = ""
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    pdf_text += extracted_text + " "
        
        if not pdf_text.strip():
            return jsonify({"error": "Could not extract text from PDF"}), 400
        
        # Convert text to speech
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
        speech_config.speech_synthesis_voice_name = AVAILABLE_VOICES.get(voice)
        
        # Generate unique file name
        file_id = str(uuid.uuid4())
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}.wav")
        
        # Configure audio output
        audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_file_path)
        
        # Create synthesizer and generate speech
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_text_async(pdf_text).get()
        
        # Clean up PDF file
        os.remove(pdf_path)
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return jsonify({
                "status": "success",
                "message": "PDF processed successfully",
                "text": pdf_text[:1000] + ("..." if len(pdf_text) > 1000 else ""),
                "fullTextLength": len(pdf_text),
                "audioUrl": f"/api/audio/{file_id}"
            })
        else:
            error_details = result.cancellation_details.error_details if result.cancellation_details else "Unknown error"
            return jsonify({"error": f"Speech synthesis failed: {error_details}"}), 500
    
    except Exception as e:
        return jsonify({"error": f"Error processing PDF: {str(e)}"}), 500

@app.route('/api/audio/<file_id>', methods=['GET'])
def get_audio(file_id):
    # Sanitize the file_id to prevent directory traversal
    file_id = secure_filename(file_id)
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}.wav")
    
    if os.path.exists(audio_path):
        return send_file(audio_path, mimetype='audio/wav', as_attachment=False)
    else:
        return jsonify({"error": "Audio file not found"}), 404

if __name__ == '__main__':
    # For development only - use proper WSGI server in production
    app.run(debug=True, port=5000)