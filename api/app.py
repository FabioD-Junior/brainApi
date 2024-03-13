from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Endpoint de Login
@app.route('/auth/login', methods=['POST'])
def login():
    username = request.headers.get('username')
    secret = request.headers.get('secret')
    if username and secret:
        return jsonify(token='eyJhbGciOiJIUd2VyIn0.NDFAApMqRBwacpLumnyC_p7IWWmmWEFmXJIVkRoIA-I')
    else:
        return {"message": "Wrong Credentials. Try Again"}, 400

# Endpoint de Simulação
@app.route('/bot/simulate', methods=['GET'])
def simulate():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1] if auth_header and auth_header.startswith("Bearer ") else None
    if not token or token != 'eyJhbGciOiJIUd2VyIn0.NDFAApMqRBwacpLumnyC_p7IWWmmWEFmXJIVkRoIA-I':
        return {"message": "Invalid or missing token"}, 401
    
    assets = pd.read_csv("save_action_memory.csv")
    data = {
        'asset_history': assets.to_json(),
        'current_balance': 10000,
        'asset_value': 15000,
        'sharpe_ratio': 1.25
    }
    
    return jsonify(data)

# Endpoint do Chatbot
@app.route('/chatbot/ask', methods=['GET'])
def ask():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1] if auth_header and auth_header.startswith("Bearer ") else None
    if not token or token != 'eyJhbGciOiJIUd2VyIn0.NDFAApMqRBwacpLumnyC_p7IWWmmWEFmXJIVkRoIA-I':
        return {"message": "Invalid or missing token"}, 401
    
    user_message = request.args.get('user_message')
    return jsonify({'bot_message': f"Mocked response to '{user_message}'"})
