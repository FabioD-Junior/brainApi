from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

 
@app.route('/auth/login', methods=['POST'])
def login():
    username = request.headers.get('username')
    secret = request.headers.get('secret')
    if username and secret:
        return jsonify(token='eyJhbGciOiJIUd2VyIn0.NDFAApMqRBwacpLumnyC_p7IWWmmWEFmXJIVkRoIA-I')
    else:
        return {"message": "Wrong Credentials. Try Again"}, 400

 
@app.route('/bot/simulate', methods=['GET'])
def simulate():
    
    ## Autentication
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1] if auth_header and auth_header.startswith("Bearer ") else None
    if not token or token != 'eyJhbGciOiJIUd2VyIn0.NDFAApMqRBwacpLumnyC_p7IWWmmWEFmXJIVkRoIA-I':
        return {"message": "Invalid or missing token"}, 401
    
    
    ## Runing simulation
    asset_history, current_balance, asset_value = run_simulation(request.args.get('agent_path'),
                                                                 request.args.get('agent_type'),
                                                                 request.args.get('data_path'),
                                                                 request.args.get('trade_limit'),
                                                                 request.args.get('buy_upper_limit'),
                                                                 request.args.get('sell_upper_limit'),
                                                                 request.args.get('initial_amount'),
                                                                 request.args.get('start_date'),
                                                                 request.args.get('env'),
                                                                 request.args.get('end_date'),
                                                                 request.args.get('symbol'),
                                                                 request.args.get('user'),
                                                                 request.args.get('resume_session'),
                                                                 request.args.get('orientation')
                                                                )
        
    
    assets = pd.read_csv("save_action_memory.csv")
    data = {
        'asset_history'  : asset_history,
        'current_balance': current_balance,
        'asset_value'    : asset_value,
        'sharpe_ratio'   : 0
    }
    
    return jsonify(data)

 
@app.route('/chatbot/ask', methods=['GET'])
def ask():
    ## Autentication
    auth_header = request.headers.get('Authorization')
    
    token      = auth_header.split(" ")[1] if auth_header and auth_header.startswith("Bearer ") else None
    
    if not token or token != 'eyJhbGciOiJIUd2VyIn0.NDFAApMqRBwacpLumnyC_p7IWWmmWEFmXJIVkRoIA-I':
        return {"message": "Invalid or missing token"}, 401
    
    ## Message
    user_message = request.args.get('user_message')
    return jsonify({'bot_message': f"Mocked response to '{user_message}'"})


def run_simulation(agent_path,agent_type,data_path,                    
                   trade_limit,buy_upper_limit, sell_upper_limit,       
                   initial_amount,start_date,env,                
                   end_date,symbol,user, resume_session,orientation):
                   
    from brainLib.brainTrader import GenericTrader
    import pandas as pd

    trader = GenericTrader()
      
    # All Tickers 
    if symbol =="Dow30":
        symbol =  ""
        
    simulation_args =  {"agent_path"    : "agents/"+agent_path+".mdl",
                        "agent_type"    : agent_type,
                        "data_path"     : data_path,
                        "trade_limit"   : trade_limit,
                        "initial_amount": str(initial_amount),
                        "start_date"    : start_date,
                        "env"           : "",
                        "end_date"      : end_date,
                        "symbol"        : symbol,
                        "user"          : user,
                        "resume_session": False
                       }

    account, actions,env = trader.start_simulation(**simulation_args)   

    
    memory        = pd.read_csv("results/state_memory.csv")
    #data          = pd.read_csv("results/asset_memory.csv")
    account_info  = pd.read_csv("results/account_value.csv")
    balance       = memory["money"].iloc[-1]
    account_value = account_info["account_value"].iloc[-1] 
    
    
    return memory.to_json(orient=orientation), balance, account_value
