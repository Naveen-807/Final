import os
import requests
from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="frontend/build", template_folder="frontend/build")
CORS(app)

# Load WebChat Secret from environment variable
WEBCHAT_SECRET = os.getenv("7tlWEiTwjIsOKxLgdo8WIviFNEBBdoivYIp7CFYYIV0j8NBe7GTQJQQJ99BBACHYHv6AArohAAABAZBS75uW.2IVzK9IgeeE2AJBZVUWnugQoBPjOLlC1gTZJaKAGK3XCIg1XonDDJQQJ99BBACHYHv6AArohAAABAZBS4DZr2IVzK9IgeeE2AJBZVUWnugQoBPjOLlC1gTZJaKAGK3XCIg1XonDDJQQJ99BBACHYHv6AArohAAABAZBS75uW.2IVzK9IgeeE2AJBZVUWnugQoBPjOLlC1gTZJaKAGK3XCIg1XonDDJQQJ99BBACHYHv6AArohAAABAZBS4DZr2IVzK9IgeeE2AJBZVUWnugQoBPjOLlC1gTZJaKAGK3XCIg1XonDDJQQJ99BBACHYHv6AArohAAABAZBS75uW.2IVzK9IgeeE2AJBZVUWnugQoBPjOLlC1gTZJaKAGK3XCIg1XonDDJQQJ99BBACHYHv6AArohAAABAZBS4DZr2IVzK9IgeeE2AJBZVUWnugQoBPjOLlC1gTZJaKAGK3XCIg1XonDDJQQJ99BBACHYHv6AArohAAABAZBS75uW.2IVzK9IgeeE2AJBZVUWnugQoBPjOLlC1gTZJaKAGK3XCIg1XonDDJQQJ99BBACHYHv6AArohAAABAZBS4DZr2IVzK9IgeeE2AJBZVUWnugQoBPjOLlC1gTZJaKAGK3XCIg1XonDDJQQJ99BBACHYHv6AArohAAABAZBS75uW.2IVzK9IgeeE2AJBZVUWnugQoBPjOLlC1gTZJaKAGK3XCIg1XonDDJQQJ99BBACHYHv6AArohAAABAZBS4DZr2IVzK9IgeeE2AJBZVUWnugQo")
DIRECT_LINE_URL = "https://directline.botframework.com/v3/directline/tokens/generate"

@app.route("/api/get_token", methods=["GET"])
def get_direct_line_token():
    """
    Generates a Direct Line token for Microsoft Bot Framework WebChat.
    """
    if not WEBCHAT_SECRET:
        return jsonify({"error": "WEBCHAT_SECRET is missing!"}), 500

    headers = {
        "Authorization": f"Bearer {WEBCHAT_SECRET}",
        "Content-Type": "application/json"
    }

    response = requests.post(DIRECT_LINE_URL, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Failed to get token", "status": response.status_code}), response.status_code

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    """
    Serves the React frontend built inside Flask.
    """
    if path and os.path.exists(f"frontend/build/{path}"):
        return send_from_directory("frontend/build", path)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
