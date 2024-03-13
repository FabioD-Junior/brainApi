from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/auth/login', methods=['POST'])
def login():
    username = request.headers.get('username')
    secret = request.headers.get('secret')
    if username and secret:
        return jsonify(token="mocked_token")
    else:
        return jsonify(message="credentials_missing"), 400

@app.route('/bot/simulate', methods=['GET'])
def simulate():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1] if auth_header and auth_header.startswith("Bearer ") else None
    if not token or token != "mocked_token":
        return jsonify(message="invalid_or_missing_token"), 401
    
    # Mocked data for simulation response
    data = {
        'result': ['simulation_result'],
        'details': ['Simulation details here'],
        'current_balance': 10000,
        'asset_value': 15000,
        'sharpe_ratio': 1.25
    }
    df = pd.DataFrame([data])
    
    return jsonify(df.to_dict(orient="records")[0])

@app.route('/chatbot/ask', methods=['GET'])
def ask():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1] if auth_header and auth_header.startswith("Bearer ") else None
    if not token or token != "mocked_token":
        return jsonify(message="invalid_or_missing_token"), 401
    
    user_message = request.args.get('user_message')
    return jsonify(bot_message=f"Mocked response to '{user_message}'")
