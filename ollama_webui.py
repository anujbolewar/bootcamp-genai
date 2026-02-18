#!/usr/bin/env python3
"""
Simple Web UI for Ollama
Access at: http://localhost:8080
"""

import json
import requests
from flask import Flask, render_template_string, request, jsonify, Response
import threading

app = Flask(__name__)

OLLAMA_API = "http://localhost:11434"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Ollama Chat</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #1a1a1a; color: #fff; }
        .container { max-width: 900px; margin: 0 auto; padding: 20px; height: 100vh; display: flex; flex-direction: column; }
        h1 { text-align: center; padding: 20px; background: #2d2d2d; border-radius: 10px; margin-bottom: 20px; }
        .model-selector { margin-bottom: 20px; }
        select { padding: 10px; width: 100%; font-size: 16px; background: #2d2d2d; color: #fff; border: 2px solid #444; border-radius: 5px; }
        .chat-box { flex: 1; background: #2d2d2d; border-radius: 10px; padding: 20px; overflow-y: auto; margin-bottom: 20px; }
        .message { margin-bottom: 15px; padding: 10px; border-radius: 8px; }
        .user { background: #0066cc; text-align: right; }
        .assistant { background: #444; text-align: left; }
        .input-area { display: flex; gap: 10px; }
        input[type="text"] { flex: 1; padding: 15px; font-size: 16px; background: #2d2d2d; color: #fff; border: 2px solid #444; border-radius: 5px; }
        button { padding: 15px 30px; font-size: 16px; background: #0066cc; color: #fff; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0052a3; }
        button:disabled { background: #666; cursor: not-allowed; }
        .loading { text-align: center; color: #888; padding: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🦙 Ollama Chat Interface</h1>
        
        <div class="model-selector">
            <select id="model">
                <option value="">Loading models...</option>
            </select>
        </div>
        
        <div class="chat-box" id="chat"></div>
        
        <div class="input-area">
            <input type="text" id="prompt" placeholder="Type your message..." onkeypress="if(event.key==='Enter')sendMessage()">
            <button onclick="sendMessage()" id="sendBtn">Send</button>
            <button onclick="clearChat()">Clear</button>
        </div>
    </div>

    <script>
        let chatHistory = [];
        
        // Load available models
        fetch('/api/models')
            .then(r => r.json())
            .then(data => {
                const select = document.getElementById('model');
                select.innerHTML = '';
                data.models.forEach(m => {
                    const option = document.createElement('option');
                    option.value = m.name;
                    option.textContent = m.name + ' (' + formatSize(m.size) + ')';
                    select.appendChild(option);
                });
            });
        
        function formatSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1024*1024) return (bytes/1024).toFixed(0) + ' KB';
            if (bytes < 1024*1024*1024) return (bytes/(1024*1024)).toFixed(0) + ' MB';
            return (bytes/(1024*1024*1024)).toFixed(2) + ' GB';
        }
        
        function addMessage(role, content) {
            const chatBox = document.getElementById('chat');
            const msgDiv = document.createElement('div');
            msgDiv.className = 'message ' + role;
            msgDiv.textContent = content;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
        async function sendMessage() {
            const prompt = document.getElementById('prompt');
            const model = document.getElementById('model').value;
            const sendBtn = document.getElementById('sendBtn');
            
            if (!prompt.value.trim() || !model) return;
            
            const userMessage = prompt.value;
            addMessage('user', userMessage);
            prompt.value = '';
            sendBtn.disabled = true;
            
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'loading';
            loadingDiv.textContent = 'Thinking...';
            document.getElementById('chat').appendChild(loadingDiv);
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({model: model, prompt: userMessage, history: chatHistory})
                });
                
                loadingDiv.remove();
                
                if (response.ok) {
                    const data = await response.json();
                    addMessage('assistant', data.response);
                    chatHistory.push({role: 'user', content: userMessage});
                    chatHistory.push({role: 'assistant', content: data.response});
                } else {
                    addMessage('assistant', 'Error: ' + response.statusText);
                }
            } catch (error) {
                loadingDiv.remove();
                addMessage('assistant', 'Error: ' + error.message);
            }
            
            sendBtn.disabled = false;
        }
        
        function clearChat() {
            document.getElementById('chat').innerHTML = '';
            chatHistory = [];
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/models')
def get_models():
    try:
        response = requests.get(f"{OLLAMA_API}/api/tags")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        model = data.get('model')
        prompt = data.get('prompt')
        
        response = requests.post(
            f"{OLLAMA_API}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.ok:
            result = response.json()
            return jsonify({"response": result.get('response', '')})
        else:
            return jsonify({"error": "Ollama API error"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🦙 Ollama Web UI Starting...")
    print("="*50)
    print(f"\n✅ Access the interface at: http://localhost:8080")
    print(f"✅ Ollama API: {OLLAMA_API}")
    print("\nPress Ctrl+C to stop\n")
    app.run(host='0.0.0.0', port=8080, debug=False)
