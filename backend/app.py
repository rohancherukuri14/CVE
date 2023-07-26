from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/api/chatbot', methods=['POST'])
def run_chatbot():
    data = request.get_json()
    user_message = data.get('message')

    # Run the Python script (example: my_script.py) with user_message as an argument
    result = subprocess.run(['python3', '../my_script.py', user_message], capture_output=True, text=True)

    return jsonify({'message': result.stdout.strip()})

if __name__ == '__main__':
    app.run(debug=True)