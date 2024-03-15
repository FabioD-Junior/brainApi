
from flask import Flask, request, jsonify
import pandas as pd
from flask_restx import Api, Resource, fields, Namespace

app = Flask(__name__)
api = Api(app, version='1.0', title='Br@in API',
          description='Br@ain API - Academic projet for a stocktrading bot.<br> This API provides authentication, trading simulation and chatbot communication')

 
ns_auth = Namespace('auth', description='Authentication endpoints')
api.add_namespace(ns_auth, path='/auth')

@ns_auth.route('/login')
class Login(Resource):
    def post(self):
        username = request.headers.get('username')
        secret   = request.headers.get('secret')
        
        if username and secret:
            return jsonify(token='eyJhbGciOiJIUd2VyIn0.NDFAApMqRBwacpLumnyC_p7IWWmmWEFmXJIVkRoIA-I' )
        else:
            return {"message": "Wrong Credentials. Try Again"}, 400

 
ns_bot = Namespace('bot', description='AirBot Simulation')
api.add_namespace(ns_bot, path='/bot')
 
simulation_response_model = api.model('SimulationResponse', {
    'asset_history'  : fields.Raw  (description = '> Assets returned'),
    'current_balance': fields.Float(description = '> Current balance'),
    'asset_value'    : fields.Float(description = '> Total Asset value'),
    'sharpe_ratio'   : fields.Float(description = '> Sharpe Ratio ')
})

@ns_bot.route('/simulate')
class Simulate(Resource):
    @api.doc(params={'agent_path'      : 'Path of the agent',
                     'agent_type'      : 'Type of the agent',
                     'data_path'       : 'Path of the basedataset',
                     'trade_limit'     : 'Trade limit per symbol',
                     'buy_upper_limit' : 'Buy upper limit per transaction',
                     'sell_upper_limit': 'Sell upper limit per transaction',
                     'initial_amount'  : 'Initial amount of money',
                     'start_date'      : 'Start day for the simulation',
                     'env'             : 'Environment',
                     'end_date'        : 'Final date for the simulation',
                     'symbol'          : 'Symbol (Aka Ticker)',
                     'user'            : 'User id (usually a hash code)',
                     'resume_session'  : 'Resume session'})
    @ns_bot.marshal_with(simulation_response_model)
    def get(self):
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
        
        return data

# Chatbot Namespace
ns_chatbot = Namespace('chatbot', description='Chatbot interaction')
api.add_namespace(ns_chatbot, path='/chatbot')

@ns_chatbot.route('/ask')
class Ask(Resource):
    @api.doc(params={'user_message': 'Message from the user'}, security='Bearer')
    @api.response(200, 'Success', model=api.model('BotResponse', {'bot_message': fields.String(description='Response from the bot')}))
    def get(self):
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1] if auth_header and auth_header.startswith("Bearer ") else None
        if not token or token != 'eyJhbGciOiJIUd2VyIn0.NDFAApMqRBwacpLumnyC_p7IWWmmWEFmXJIVkRoIA-I':
            return {"message": "Invalid or missing token"}, 401
        
        user_message = request.args.get('user_message')
        

        return {'bot_message': f"Mocked response to '{user_message}'"}

if __name__ == '__main__':
    app.run(debug=True))

