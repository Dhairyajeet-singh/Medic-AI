from flask import Flask, request, jsonify,render_template, url_for
import argparse
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
api = os.getenv("OPENAI_API_KEY")
@app.route('/')
def home():
    return render_template('index.html')
def generate_report(user_input):
    from openai import OpenAI
    client = OpenAI(api_key=api)
    prompt = f"""
You are a helpful medical research assistant, think like a doctor.
A patient reports the following symptoms: {user_input}.
Provide:
- A brief summary
- Suggested diagnostic tests
- Possible diseases grouped as high, medium, and low probability
Respond in plain text, no JSON.
"""

    response = client.responses.create(
        model="gpt-4o-mini",  
        input=prompt
    )
    return response.output_text


@app.route('/chat', methods=["GET", "POST"])
def chat():
    output=None
    if request.method == "POST":
        # Handle JSON input
        user_input = request.form["inputText"]
        output = generate_report(user_input)
    return render_template("chat.html", output=output)


if __name__ == "__main__": 
    app.run(debug=False, port=5000)