import pytest
import requests

BASE_URL = "http://localhost:5000"
API_KEY = "test-key-123"
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

@pytest.mark.functional
class TestStocks:
    @pytest.mark.positive
    def test_get_all_stocks(self):
        response = requests.get(f"{BASE_URL}/stocks")
        assert response.status_code == 200
        assert len(response.json()) > 0
    
    @pytest.mark.positive
    def test_get_specific_stock(self):
        response = requests.get(f"{BASE_URL}/stocks/AAPL")
        assert response.status_code == 200
        assert response.json()["symbol"] == "AAPL"
    
    @pytest.mark.negative
    def test_get_invalid_stock(self):
        response = requests.get(f"{BASE_URL}/stocks/INVALID")
        assert response.status_code == 404

@pytest.mark.functional
class TestAuthentication:
    @pytest.mark.negative
    def test_missing_api_key(self):
        response = requests.get(f"{BASE_URL}/trades")
        assert response.status_code == 401
    
    @pytest.mark.negative
    def test_invalid_api_key(self):
        headers = {"X-API-Key": "invalid-key"}
        response = requests.get(f"{BASE_URL}/trades", headers=headers)
        assert response.status_code == 401
    
    @pytest.mark.positive
    def test_valid_api_key_demo(self):
        headers = {"X-API-Key": "demo-key-456", "Content-Type": "application/json"}
        response = requests.get(f"{BASE_URL}/trades", headers=headers)
        assert response.status_code == 200
    
    @pytest.mark.negative
    def test_auth_on_post_trade(self):
        data = {"symbol": "AAPL", "quantity": 5, "action": "buy"}
        response = requests.post(f"{BASE_URL}/trades", json=data)
        assert response.status_code == 401
    
    @pytest.mark.negative
    def test_auth_on_portfolio(self):
        response = requests.get(f"{BASE_URL}/portfolio")
        assert response.status_code == 401

@pytest.mark.functional
class TestAccount:
    @pytest.mark.positive
    def test_get_balance(self):
        response = requests.get(f"{BASE_URL}/account/balance", headers=HEADERS)
        assert response.status_code == 200
        assert "balance" in response.json()
    
    @pytest.mark.positive
    def test_deposit_funds(self):
        data = {"amount": 1000}
        response = requests.post(f"{BASE_URL}/account/deposit", json=data, headers=HEADERS)
        assert response.status_code == 200
        assert response.json()["deposited"] == 1000
    
    @pytest.mark.positive
    def test_withdraw_funds(self):
        data = {"amount": 500}
        response = requests.post(f"{BASE_URL}/account/withdraw", json=data, headers=HEADERS)
        assert response.status_code == 200
        assert response.json()["withdrawn"] == 500
    
    @pytest.mark.negative
    def test_withdraw_insufficient_funds(self):
        data = {"amount": 999999}
        response = requests.post(f"{BASE_URL}/account/withdraw", json=data, headers=HEADERS)
        assert response.status_code == 400

@pytest.mark.functional
class TestTrades:
    @pytest.mark.positive
    def test_execute_buy_trade(self):
        data = {"symbol": "AAPL", "quantity": 5, "action": "buy"}
        response = requests.post(f"{BASE_URL}/trades", json=data, headers=HEADERS)
        assert response.status_code == 201
        assert response.json()["symbol"] == "AAPL"
        assert response.json()["action"] == "buy"
    
    @pytest.mark.positive
    def test_get_all_trades(self):
        response = requests.get(f"{BASE_URL}/trades", headers=HEADERS)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    @pytest.mark.negative
    def test_execute_trade_invalid_symbol(self):
        data = {"symbol": "INVALID", "quantity": 5, "action": "buy"}
        response = requests.post(f"{BASE_URL}/trades", json=data, headers=HEADERS)
        assert response.status_code == 400
    
    @pytest.mark.negative
    def test_execute_trade_missing_fields(self):
        data = {"symbol": "AAPL"}
        response = requests.post(f"{BASE_URL}/trades", json=data, headers=HEADERS)
        assert response.status_code == 400
    
    @pytest.mark.positive
    def test_update_trade(self):
        data = {"symbol": "MSFT", "quantity": 2, "action": "buy"}
        create_response = requests.post(f"{BASE_URL}/trades", json=data, headers=HEADERS)
        trade_id = create_response.json()["id"]
        
        update_data = {"quantity": 5}
        response = requests.put(f"{BASE_URL}/trades/{trade_id}", json=update_data, headers=HEADERS)
        assert response.status_code == 200
        assert response.json()["quantity"] == 5
    
    @pytest.mark.positive
    def test_delete_trade(self):
        data = {"symbol": "GOOGL", "quantity": 1, "action": "buy"}
        create_response = requests.post(f"{BASE_URL}/trades", json=data, headers=HEADERS)
        trade_id = create_response.json()["id"]
        
        response = requests.delete(f"{BASE_URL}/trades/{trade_id}", headers=HEADERS)
        assert response.status_code == 200

@pytest.mark.functional
class TestPortfolio:
    @pytest.mark.positive
    def test_get_portfolio(self):
        response = requests.get(f"{BASE_URL}/portfolio", headers=HEADERS)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    @pytest.mark.positive
    def test_get_portfolio_value(self):
        response = requests.get(f"{BASE_URL}/portfolio/value", headers=HEADERS)
        assert response.status_code == 200
        assert "total_value" in response.json()

@pytest.mark.functional
class TestTradeWorkflow:
    @pytest.mark.positive
    def test_complete_trading_workflow(self):
        # Check initial balance
        balance_response = requests.get(f"{BASE_URL}/account/balance", headers=HEADERS)
        initial_balance = balance_response.json()["balance"]
        
        # Deposit funds
        deposit_data = {"amount": 5000}
        requests.post(f"{BASE_URL}/account/deposit", json=deposit_data, headers=HEADERS)
        
        # Execute buy trade
        trade_data = {"symbol": "TSLA", "quantity": 3, "action": "buy"}
        trade_response = requests.post(f"{BASE_URL}/trades", json=trade_data, headers=HEADERS)
        assert trade_response.status_code == 201
        
        # Check portfolio
        portfolio_response = requests.get(f"{BASE_URL}/portfolio", headers=HEADERS)
        assert len(portfolio_response.json()) > 0
        
        # Check portfolio value
        value_response = requests.get(f"{BASE_URL}/portfolio/value", headers=HEADERS)
        assert value_response.json()["total_value"] > 0
