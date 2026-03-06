import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_headers():
    return {'X-API-Key': 'test-key-123', 'Content-Type': 'application/json'}

@pytest.mark.unit
class TestStocksUnit:
    @pytest.mark.positive
    def test_get_all_stocks(self, client):
        response = client.get('/stocks')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 4
        assert any(s['symbol'] == 'AAPL' for s in data)
    
    @pytest.mark.positive
    def test_get_stock_by_symbol(self, client):
        response = client.get('/stocks/AAPL')
        assert response.status_code == 200
        data = response.get_json()
        assert data['symbol'] == 'AAPL'
        assert data['name'] == 'Apple Inc.'
        assert 'price' in data
    
    @pytest.mark.negative
    def test_get_stock_not_found(self, client):
        response = client.get('/stocks/INVALID')
        assert response.status_code == 404
        assert 'error' in response.get_json()

@pytest.mark.unit
class TestAuthenticationUnit:
    @pytest.mark.negative
    def test_no_api_key(self, client):
        response = client.get('/trades')
        assert response.status_code == 401
        assert response.get_json()['error'] == 'Invalid or missing API key'
    
    @pytest.mark.negative
    def test_invalid_api_key(self, client):
        headers = {'X-API-Key': 'wrong-key'}
        response = client.get('/trades', headers=headers)
        assert response.status_code == 401
    
    @pytest.mark.positive
    def test_valid_api_key(self, client, auth_headers):
        response = client.get('/trades', headers=auth_headers)
        assert response.status_code == 200
    
    @pytest.mark.positive
    def test_second_valid_api_key(self, client):
        headers = {'X-API-Key': 'demo-key-456'}
        response = client.get('/trades', headers=headers)
        assert response.status_code == 200
    
    @pytest.mark.negative
    def test_empty_api_key(self, client):
        headers = {'X-API-Key': ''}
        response = client.get('/trades', headers=headers)
        assert response.status_code == 401
    
    @pytest.mark.negative
    def test_auth_required_on_portfolio(self, client):
        response = client.get('/portfolio')
        assert response.status_code == 401
    
    @pytest.mark.negative
    def test_auth_required_on_account(self, client):
        response = client.get('/account/balance')
        assert response.status_code == 401

@pytest.mark.unit
class TestAccountUnit:
    @pytest.mark.positive
    def test_get_balance(self, client, auth_headers):
        response = client.get('/account/balance', headers=auth_headers)
        assert response.status_code == 200
        assert 'balance' in response.get_json()
    
    @pytest.mark.positive
    def test_deposit_valid_amount(self, client, auth_headers):
        response = client.post('/account/deposit', json={'amount': 1000}, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['deposited'] == 1000
        assert 'balance' in data
    
    @pytest.mark.negative
    def test_deposit_negative_amount(self, client, auth_headers):
        response = client.post('/account/deposit', json={'amount': -100}, headers=auth_headers)
        assert response.status_code == 400
    
    @pytest.mark.negative
    def test_deposit_missing_amount(self, client, auth_headers):
        response = client.post('/account/deposit', json={}, headers=auth_headers)
        assert response.status_code == 400
    
    @pytest.mark.positive
    def test_withdraw_valid_amount(self, client, auth_headers):
        response = client.post('/account/withdraw', json={'amount': 100}, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['withdrawn'] == 100
    
    @pytest.mark.negative
    def test_withdraw_insufficient_funds(self, client, auth_headers):
        response = client.post('/account/withdraw', json={'amount': 999999}, headers=auth_headers)
        assert response.status_code == 400
        assert 'Insufficient funds' in response.get_json()['error']

@pytest.mark.unit
class TestTradesUnit:
    @pytest.mark.positive
    def test_create_buy_trade(self, client, auth_headers):
        trade_data = {'symbol': 'AAPL', 'quantity': 5, 'action': 'buy'}
        response = client.post('/trades', json=trade_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.get_json()
        assert data['symbol'] == 'AAPL'
        assert data['quantity'] == 5
        assert data['action'] == 'buy'
        assert 'id' in data
        assert 'total' in data
    
    @pytest.mark.negative
    def test_create_trade_invalid_symbol(self, client, auth_headers):
        trade_data = {'symbol': 'INVALID', 'quantity': 5, 'action': 'buy'}
        response = client.post('/trades', json=trade_data, headers=auth_headers)
        assert response.status_code == 400
    
    @pytest.mark.negative
    def test_create_trade_invalid_action(self, client, auth_headers):
        trade_data = {'symbol': 'AAPL', 'quantity': 5, 'action': 'hold'}
        response = client.post('/trades', json=trade_data, headers=auth_headers)
        assert response.status_code == 400
    
    @pytest.mark.negative
    def test_create_trade_missing_fields(self, client, auth_headers):
        trade_data = {'symbol': 'AAPL'}
        response = client.post('/trades', json=trade_data, headers=auth_headers)
        assert response.status_code == 400
    
    @pytest.mark.negative
    def test_create_trade_negative_quantity(self, client, auth_headers):
        trade_data = {'symbol': 'AAPL', 'quantity': -5, 'action': 'buy'}
        response = client.post('/trades', json=trade_data, headers=auth_headers)
        assert response.status_code == 400
    
    @pytest.mark.positive
    def test_get_all_trades(self, client, auth_headers):
        response = client.get('/trades', headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)
    
    @pytest.mark.positive
    def test_get_trade_by_id(self, client, auth_headers):
        # Create a trade first
        trade_data = {'symbol': 'MSFT', 'quantity': 2, 'action': 'buy'}
        create_response = client.post('/trades', json=trade_data, headers=auth_headers)
        trade_id = create_response.get_json()['id']
        
        # Get the trade
        response = client.get(f'/trades/{trade_id}', headers=auth_headers)
        assert response.status_code == 200
        assert response.get_json()['id'] == trade_id
    
    @pytest.mark.negative
    def test_get_trade_not_found(self, client, auth_headers):
        response = client.get('/trades/99999', headers=auth_headers)
        assert response.status_code == 404
    
    @pytest.mark.positive
    def test_update_trade(self, client, auth_headers):
        # Create a trade
        trade_data = {'symbol': 'GOOGL', 'quantity': 3, 'action': 'buy'}
        create_response = client.post('/trades', json=trade_data, headers=auth_headers)
        trade_id = create_response.get_json()['id']
        
        # Update the trade
        update_data = {'quantity': 10}
        response = client.put(f'/trades/{trade_id}', json=update_data, headers=auth_headers)
        assert response.status_code == 200
        assert response.get_json()['quantity'] == 10
    
    @pytest.mark.positive
    def test_delete_trade(self, client, auth_headers):
        # Create a trade
        trade_data = {'symbol': 'TSLA', 'quantity': 1, 'action': 'buy'}
        create_response = client.post('/trades', json=trade_data, headers=auth_headers)
        trade_id = create_response.get_json()['id']
        
        # Delete the trade
        response = client.delete(f'/trades/{trade_id}', headers=auth_headers)
        assert response.status_code == 200
        assert 'message' in response.get_json()
    
    @pytest.mark.negative
    def test_delete_trade_not_found(self, client, auth_headers):
        response = client.delete('/trades/99999', headers=auth_headers)
        assert response.status_code == 404

@pytest.mark.unit
class TestPortfolioUnit:
    @pytest.mark.positive
    def test_get_portfolio(self, client, auth_headers):
        response = client.get('/portfolio', headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)
    
    @pytest.mark.positive
    def test_get_portfolio_value(self, client, auth_headers):
        response = client.get('/portfolio/value', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'total_value' in data
        assert isinstance(data['total_value'], (int, float))

@pytest.mark.unit
class TestBusinessLogicUnit:
    @pytest.mark.negative
    def test_insufficient_funds_for_trade(self, client, auth_headers):
        # Try to buy expensive stock without enough funds
        trade_data = {'symbol': 'MSFT', 'quantity': 1000, 'action': 'buy'}
        response = client.post('/trades', json=trade_data, headers=auth_headers)
        assert response.status_code == 400
        assert 'Insufficient funds' in response.get_json()['error']
    
    @pytest.mark.negative
    def test_sell_without_shares(self, client, auth_headers):
        # Try to sell stock we don't own
        trade_data = {'symbol': 'AAPL', 'quantity': 100, 'action': 'sell'}
        response = client.post('/trades', json=trade_data, headers=auth_headers)
        assert response.status_code == 400
        assert 'Insufficient shares' in response.get_json()['error']
    
    @pytest.mark.positive
    def test_portfolio_updates_after_buy(self, client, auth_headers):
        # Deposit funds
        client.post('/account/deposit', json={'amount': 5000}, headers=auth_headers)
        
        # Buy stock
        trade_data = {'symbol': 'AAPL', 'quantity': 5, 'action': 'buy'}
        client.post('/trades', json=trade_data, headers=auth_headers)
        
        # Check portfolio
        response = client.get('/portfolio', headers=auth_headers)
        portfolio = response.get_json()
        assert any(h['symbol'] == 'AAPL' for h in portfolio)
