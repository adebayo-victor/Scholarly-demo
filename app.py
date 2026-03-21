import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini securely on the server
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-3-flash-preview')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        # Get the user prompt from the frontend request
        data = request.json
        user_prompt = data.get("prompt")
        
        if not user_prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # Generate response using the server-side API key
        response = model.generate_content(user_prompt)
        
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
