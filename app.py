from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Function to fetch response from Gemini API
def fetch_gemini_response(prompt):
    api_key = os.getenv("GEMINI_API_KEY")  # Get API key from .env file
    if not api_key:
        return "Error: API key not found. Set GEMINI_API_KEY in the .env file."

    api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"

    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(f"{api_url}?key={api_key}", json=payload, headers=headers)
        data = response.json()

        # Debugging: Print response from API (optional)
        print("Gemini API Response:", data)

        if response.status_code == 200:
            # ✅ Extract the response text from the nested JSON structure
            gemini_response = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "No response generated.")
            )
            return gemini_response
        else:
            return f"Error: {data.get('error', {}).get('message', 'Unknown error')}"
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"

# Home route to render the frontend page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle user input and get Gemini API response
@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form.get('message')  # Get user input from form
    if not user_input:
        return jsonify(response="Error: No input provided.")

    response = fetch_gemini_response(user_input)  # Get response from Gemini API
    return jsonify(response=response)  # Return response as JSON

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
