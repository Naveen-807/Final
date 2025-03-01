from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import azure.cognitiveservices.speech as speechsdk
import os
import uuid
import pdfplumber
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Create directories for files
AUDIO_OUTPUT_DIR = "audio_output"
UPLOAD_FOLDER = "uploads"
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configuration
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Azure Configuration
speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_SPEECH_REGION", "eastus")
if not speech_key:
    raise ValueError("Missing Azure Speech API key. Set AZURE_SPEECH_KEY in environment variables.")

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

AVAILABLE_VOICES = {
    "tamil_female": "ta-IN-PallaviNeural",
    "tamil_male": "ta-IN-ValluvarNeural",
    "english_female": "en-US-JennyNeural",
    "english_male": "en-US-GuyNeural"
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    try:
        voice_key = request.form.get('voice', 'tamil_female')
        if voice_key not in AVAILABLE_VOICES:
            return jsonify({"error": "Invalid voice selection"}), 400

        text = ""
        file_path = None
        
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                text = extract_text_from_pdf(file_path)
                os.remove(file_path)
            else:
                return jsonify({"error": "Invalid file format. Only PDF files are allowed"}), 400
        else:
            data = request.get_json()
            if not data or 'text' not in data:
                return jsonify({"error": "No text or file provided"}), 400
            text = data['text'].strip()

        if not text:
            return jsonify({"error": "No text content found"}), 400

        # Generate unique filename for audio output
        audio_filename = os.path.join(AUDIO_OUTPUT_DIR, f"{uuid.uuid4()}.wav")

        # Configure speech synthesis
        speech_config.speech_synthesis_voice_name = AVAILABLE_VOICES[voice_key]
        audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_filename)
        
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, 
            audio_config=audio_config
        )

        print(f"Synthesizing text: {text}")
        result = speech_synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            response = send_file(
                audio_filename,
                mimetype="audio/wav",
                as_attachment=True,
                download_name="speech.wav"
            )
            os.remove(audio_filename)  # Clean up after sending response
            return response
        else:
            return jsonify({"error": f"Speech synthesis failed: {result.reason}"}), 500

    except Exception as e:
        print(f"Exception occurred: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/voices', methods=['GET'])
def get_voices():
    return jsonify({"voices": AVAILABLE_VOICES})

if __name__ == '__main__':
    app.run(debug=True)