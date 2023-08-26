from flask import Flask, request, jsonify
import subprocess
import openai
import sys
import utils
import json
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app, origins='http://localhost:3000', allow_headers=["Content-Type"])

def get_config_key():
    with open('../config.json') as f:
        config_data = json.load(f)
    return config_data["api_key"]

openai.api_key = get_config_key()

def add_cors_headers(response):
    # Allow requests from the specific origin (your React app's origin)
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    # Allow the Content-Type header for the preflight request
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/api/chatbot', methods=['POST', 'OPTIONS'])
def run_chatbot():
    if request.method == 'OPTIONS':
        response = jsonify({})
    else:
        data = request.get_json()
        user_message = data.get('message')

        # Run the Python script (example: my_script.py) with user_message as an argument
        result = get_response(user_message)

        response = jsonify({'message': result})

    response = add_cors_headers(response)
    return response


def get_response(code):
    message = [{"role": "system", "content" : "Provide new code to fix the vulnerabilities in the code given."},
                {"role": "user", "content" : code}]
    completion = openai.ChatCompletion.create(
        model = "ft:gpt-3.5-turbo-0613:fittedai::7rhw2sBy",
        messages = message,
    )
    return re.sub(r'(\d+\.)', r'\n\1', completion.choices[0].message["content"])


if __name__ == '__main__':
    app.run(debug=True)