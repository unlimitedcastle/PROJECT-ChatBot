import requests

def call_ollama_model(prompt, model):

    url = 'http://localhost:11434/api/chat'


    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'stream': False
    }

    response = requests.post(url, json=payload)

    data = response.json()
    return data['message']['content']