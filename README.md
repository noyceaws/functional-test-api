# 📈 Stock Trading API

A simple Flask REST API for managing stock trades - perfect for learning functional testing!

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

The API runs at `http://localhost:5000`

## Authentication

Most endpoints require an API key. Include it in the `X-API-Key` header.

**Valid API Keys:**
- `test-key-123`
- `demo-key-456`

## API Endpoints

### Get all stocks (no auth required)
```bash
GET /stocks
```

### Get a specific stock (no auth required)
```bash
GET /stocks/{symbol}
```

### Get all trades (requires auth)
```bash
GET /trades
X-API-Key: test-key-123
```

### Get a specific trade (requires auth)
```bash
GET /trades/{id}
X-API-Key: test-key-123
```

### Execute a trade (requires auth)
```bash
POST /trades
X-API-Key: test-key-123
Content-Type: application/json

{
  "symbol": "AAPL",
  "quantity": 10,
  "action": "buy"
}
```

### Update a trade (requires auth)
```bash
PUT /trades/{id}
X-API-Key: test-key-123
Content-Type: application/json

{
  "quantity": 15
}
```

### Cancel a trade (requires auth)
```bash
DELETE /trades/{id}
X-API-Key: test-key-123
```

### Get portfolio (requires auth)
```bash
GET /portfolio
X-API-Key: test-key-123
```

### Get portfolio value (requires auth)
```bash
GET /portfolio/value
X-API-Key: test-key-123
```

### Get account balance (requires auth)
```bash
GET /account/balance
X-API-Key: test-key-123
```

### Deposit funds (requires auth)
```bash
POST /account/deposit
X-API-Key: test-key-123
Content-Type: application/json

{
  "amount": 1000.00
}
```

### Withdraw funds (requires auth)
```bash
POST /account/withdraw
X-API-Key: test-key-123
Content-Type: application/json

{
  "amount": 500.00
}
```

## Example Usage

```bash
# Get all available stocks (no auth)
curl http://localhost:5000/stocks

# Get specific stock (no auth)
curl http://localhost:5000/stocks/AAPL

# Deposit funds (with auth)
curl -X POST http://localhost:5000/account/deposit \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-key-123" \
  -d '{"amount":10000}'

# Execute a buy trade (with auth)
curl -X POST http://localhost:5000/trades \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-key-123" \
  -d '{"symbol":"AAPL","quantity":10,"action":"buy"}'

# Get all trades (with auth)
curl -H "X-API-Key: test-key-123" http://localhost:5000/trades

# Update a trade (with auth)
curl -X PUT http://localhost:5000/trades/1 \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-key-123" \
  -d '{"quantity":15}'

# Get portfolio (with auth)
curl -H "X-API-Key: test-key-123" http://localhost:5000/portfolio

# Get portfolio value (with auth)
curl -H "X-API-Key: test-key-123" http://localhost:5000/portfolio/value

# Get account balance (with auth)
curl -H "X-API-Key: test-key-123" http://localhost:5000/account/balance

# Cancel a trade (with auth)
curl -X DELETE -H "X-API-Key: test-key-123" http://localhost:5000/trades/1
```

## Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run unit tests (no server needed)
pytest tests/unit/ -v

# Run functional tests (requires running server)
# Start the API server (in one terminal)
python app.py

# Run tests (in another terminal)
pytest tests/functional/ -v

# Run all tests
pytest tests/ -v

# Run tests by marker
pytest -m unit -v
pytest -m functional -v
pytest -m positive -v
pytest -m negative -v
```
