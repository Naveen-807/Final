from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Set up Gemini API key (replace with actual API key)
genai.configure(api_key="AIzaSyDQ4yAsKyz6_z9ypE7B2OzW0b3oeiwByvk")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"reply": "I didn't understand that."})
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(user_message)
        bot_reply = response.text if hasattr(response, "text") else "Sorry, I couldn't generate a response."
    except Exception as e:
        bot_reply = "Sorry, an error occurred."
        print("Error:", e)
            
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
