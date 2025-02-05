from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Load API Keys from Environment Variables
FUB_API_KEY = os.getenv("FUB_API_KEY")
CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY")

@app.route('/')
def home():
    return "FUB - ChatGPT API is running!"

@app.route('/process_lead', methods=['POST'])
def process_lead():
    data = request.json
    lead_name = data.get('name', 'Client')
    lead_stage = data.get('stage', 'New Lead')

    prompt = f"Write a follow-up message for {lead_name} who is at the {lead_stage} stage."

    chatgpt_response = requests.post(
        "https://api.openai.com/v1/completions",
        headers={"Authorization": f"Bearer {CHATGPT_API_KEY}"},
        json={"model": "gpt-4", "prompt": prompt, "max_tokens": 100}
    )

    chat_message = chatgpt_response.json().get("choices", [{}])[0].get("text", "").strip()

    return jsonify({"ChatGPT Response": chat_message})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
