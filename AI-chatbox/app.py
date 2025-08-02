import json
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question', '')
    print("Received question:", question)

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'gemma3:latest',
                'prompt': question,
                'stream': True
            },
            stream=True
        )

        final_answer = ""
        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                print("Raw line:", decoded)
                try:
                    data = json.loads(decoded)
                    if "response" in data:
                        final_answer += data["response"]
                        print("Partial response:", data["response"])
                except json.JSONDecodeError:
                    print("Skipped non-json line.")

        print("Full response:", final_answer)
        return jsonify({'answer': final_answer})

    except Exception as e:
        print("Error in /ask:", e)
        return jsonify({'answer': f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
