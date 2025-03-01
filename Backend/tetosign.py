from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allows React to communicate with Flask

# Path to your GIFs folder
GIFS_FOLDER = r"C:\Users\mathe\OneDrive\Desktop\Hackathon\Hackathon\GIFS"

@app.route("/get_gif", methods=["GET"])
def get_gif():
    word = request.args.get("word", "").strip().lower()
    print(f"Received request for word: {word}")  # Debugging print

    for filename in os.listdir(GIFS_FOLDER):
        print(f"Checking file: {filename}")  # Debugging print
        if filename.lower().startswith(word) and filename.endswith(".gif"):
            print(f"GIF found: {filename}")  # Debugging print
            return jsonify({"gif_url": f"http://127.0.0.1:5000/static/gifs/{filename}"})  # Full URL

    print("GIF not found!")  # Debugging print
    return jsonify({"error": "GIF not found"}), 404

# Serve GIFs
@app.route("/static/gifs/<path:filename>")
def serve_gif(filename):
    return send_from_directory(GIFS_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Set port explicitly
