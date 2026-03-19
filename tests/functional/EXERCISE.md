# 🧪 Exercise: Write a Functional Test for GET /stocks/{symbol}/history

A new endpoint has been added to the API. Your task is to write functional tests for it.

## The Endpoint

```
GET /stocks/{symbol}/history
```

- No authentication required
- Returns 5 months of price history for a given stock symbol

## Example Request

```bash
curl http://localhost:5000/stocks/AAPL/history
```

## Example Response

```json
{
  "symbol": "AAPL",
  "history": [
    { "date": "2024-01-01", "price": 149.18 },
    { "date": "2024-02-01", "price": 157.95 },
    { "date": "2024-03-01", "price": 166.73 },
    { "date": "2024-04-01", "price": 171.99 },
    { "date": "2024-05-01", "price": 175.50 }
  ]
}
```

## Your Task

Open `tests/functional/test_stock_history.py` and implement the following 3 tests:

### 1. `test_get_stock_history` (positive)
- Make a `GET` request to `/stocks/AAPL/history`
- Assert the response status code is `200`
- Assert the response contains a `symbol` field equal to `"AAPL"`
- Assert the response contains a `history` field
- Assert `history` is a list with more than 0 items
- Assert each item in the list has a `date` and `price` field

### 2. `test_get_history_invalid_symbol` (negative)
- Make a `GET` request to `/stocks/INVALID/history`
- Assert the response status code is `404`
- Assert the response contains an `error` field

### 3. `test_get_history_no_auth_required` (positive)
- Make a `GET` request to `/stocks/MSFT/history` with **no API key**
- Assert the response status code is `200`

## Running Your Tests

Start the API server in one terminal:
```bash
python app.py
```

Run your tests in another terminal:
```bash
pytest tests/functional/test_stock_history.py -v
```

## Hints

- Use the `requests` library to make HTTP requests
- A `GET` request with no headers looks like: `requests.get(f"{BASE_URL}/stocks/AAPL/history")`
- To check a field exists in a response: `assert "symbol" in response.json()`
- To check a list is not empty: `assert len(response.json()["history"]) > 0`
- To check every item in a list has a field: `assert all("date" in item for item in history)`
