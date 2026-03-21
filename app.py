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
def generate():
    try:
        data = request.json
        user_prompt = data.get("prompt")
        system_instructions = data.get("system_instruction", "You are a helpful academic assistant.")

        # Re-initialize model with the specific system instruction sent from frontend
        dynamic_model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=system_instructions
        )

        response = dynamic_model.generate_content(user_prompt)
        
        # Return the same structure your frontend expects
        return jsonify({
            "candidates": [{
                "content": {"parts": [{"text": response.text}]}
            }]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
