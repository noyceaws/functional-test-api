from flask import Flask, jsonify, request
from datetime import datetime
from functools import wraps

app = Flask(__name__)

API_KEYS = {'test-key-123', 'demo-key-456'}
accounts = {'test-key-123': 10000.0, 'demo-key-456': 10000.0}

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key not in API_KEYS:
            return jsonify({'error': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated

stocks = {
    'AAPL': {'symbol': 'AAPL', 'name': 'Apple Inc.', 'price': 175.50},
    'GOOGL': {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'price': 140.25},
    'MSFT': {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'price': 380.00},
    'TSLA': {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'price': 245.75}
}

trades = {}
portfolio = {}
next_id = 1

@app.route('/')
def home():
    return jsonify({'message': 'Stock Trading API', 'version': '1.0'})

@app.route('/stocks', methods=['GET'])
def get_stocks():
    return jsonify(list(stocks.values()))

@app.route('/stocks/<symbol>', methods=['GET'])
def get_stock(symbol):
    symbol = symbol.upper()
    if symbol not in stocks:
        return jsonify({'error': 'Stock not found'}), 404
    return jsonify(stocks[symbol])

@app.route('/trades', methods=['GET'])
@require_api_key
def get_trades():
    return jsonify(list(trades.values()))

@app.route('/trades/<int:trade_id>', methods=['GET'])
@require_api_key
def get_trade(trade_id):
    trade = trades.get(trade_id)
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    return jsonify(trade)

@app.route('/trades', methods=['POST'])
@require_api_key
def execute_trade():
    global next_id
    api_key = request.headers.get('X-API-Key')
    data = request.get_json()
    
    if not data or 'symbol' not in data or 'quantity' not in data or 'action' not in data:
        return jsonify({'error': 'Symbol, quantity, and action are required'}), 400
    
    symbol = data['symbol'].upper()
    if symbol not in stocks:
        return jsonify({'error': 'Invalid stock symbol'}), 400
    
    if data['action'] not in ['buy', 'sell']:
        return jsonify({'error': 'Action must be buy or sell'}), 400
    
    quantity = data['quantity']
    if quantity <= 0:
        return jsonify({'error': 'Quantity must be positive'}), 400
    
    price = stocks[symbol]['price']
    total = price * quantity
    
    if data['action'] == 'buy' and accounts[api_key] < total:
        return jsonify({'error': 'Insufficient funds'}), 400
    
    if data['action'] == 'sell':
        if symbol not in portfolio or portfolio[symbol] < quantity:
            return jsonify({'error': 'Insufficient shares'}), 400
    
    trade = {
        'id': next_id,
        'symbol': symbol,
        'quantity': quantity,
        'action': data['action'],
        'price': price,
        'total': total,
        'timestamp': datetime.now().isoformat(),
        'status': 'completed'
    }
    
    trades[next_id] = trade
    
    if symbol not in portfolio:
        portfolio[symbol] = 0
    
    if data['action'] == 'buy':
        portfolio[symbol] += quantity
        accounts[api_key] -= total
    else:
        portfolio[symbol] -= quantity
        accounts[api_key] += total
    
    next_id += 1
    return jsonify(trade), 201

@app.route('/trades/<int:trade_id>', methods=['PUT'])
@require_api_key
def update_trade(trade_id):
    if trade_id not in trades:
        return jsonify({'error': 'Trade not found'}), 404
    
    data = request.get_json()
    trade = trades[trade_id]
    
    if 'quantity' in data:
        trade['quantity'] = data['quantity']
        trade['total'] = trade['price'] * data['quantity']
    
    return jsonify(trade)

@app.route('/trades/<int:trade_id>', methods=['DELETE'])
@require_api_key
def cancel_trade(trade_id):
    if trade_id not in trades:
        return jsonify({'error': 'Trade not found'}), 404
    
    deleted = trades.pop(trade_id)
    return jsonify({'message': 'Trade cancelled', 'trade': deleted})

@app.route('/portfolio', methods=['GET'])
@require_api_key
def get_portfolio():
    holdings = [{'symbol': sym, 'quantity': qty, 'current_price': stocks[sym]['price'], 'value': qty * stocks[sym]['price']} 
                for sym, qty in portfolio.items() if qty > 0]
    return jsonify(holdings)

@app.route('/portfolio/value', methods=['GET'])
@require_api_key
def get_portfolio_value():
    total_value = sum(qty * stocks[sym]['price'] for sym, qty in portfolio.items() if qty > 0)
    return jsonify({'total_value': total_value})

@app.route('/account/balance', methods=['GET'])
@require_api_key
def get_balance():
    api_key = request.headers.get('X-API-Key')
    return jsonify({'balance': accounts[api_key]})

@app.route('/account/deposit', methods=['POST'])
@require_api_key
def deposit():
    api_key = request.headers.get('X-API-Key')
    data = request.get_json()
    
    if not data or 'amount' not in data:
        return jsonify({'error': 'Amount is required'}), 400
    
    amount = data['amount']
    if amount <= 0:
        return jsonify({'error': 'Amount must be positive'}), 400
    
    accounts[api_key] += amount
    return jsonify({'balance': accounts[api_key], 'deposited': amount})

@app.route('/account/withdraw', methods=['POST'])
@require_api_key
def withdraw():
    api_key = request.headers.get('X-API-Key')
    data = request.get_json()
    
    if not data or 'amount' not in data:
        return jsonify({'error': 'Amount is required'}), 400
    
    amount = data['amount']
    if amount <= 0:
        return jsonify({'error': 'Amount must be positive'}), 400
    
    if accounts[api_key] < amount:
        return jsonify({'error': 'Insufficient funds'}), 400
    
    accounts[api_key] -= amount
    return jsonify({'balance': accounts[api_key], 'withdrawn': amount})

if __name__ == '__main__':
    app.run(debug=True)
