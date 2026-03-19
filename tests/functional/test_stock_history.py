# 🧪 Exercise: Write a Functional Test for GET /stocks/{symbol}/history
#
# A new endpoint has been added to the API:
#
#   GET /stocks/{symbol}/history
#
# This endpoint does NOT require authentication.
#
# Example request:
#   curl http://localhost:5000/stocks/AAPL/history
#
# Example response:
#   {
#     "symbol": "AAPL",
#     "history": [
#       { "date": "2024-01-01", "price": 149.18 },
#       { "date": "2024-02-01", "price": 157.95 },
#       { "date": "2024-03-01", "price": 166.73 },
#       { "date": "2024-04-01", "price": 171.99 },
#       { "date": "2024-05-01", "price": 175.50 }
#     ]
#   }
#
# Your Task:
# ----------
# Complete the test class below by implementing the following test methods:
#
#   1. test_get_stock_history (positive)
#      - Make a GET request to /stocks/AAPL/history
#      - Assert the response status code is 200
#      - Assert the response contains a "symbol" field equal to "AAPL"
#      - Assert the response contains a "history" field
#      - Assert the "history" field is a list with more than 0 items
#      - Assert each item in the history list has a "date" and "price" field
#
#   2. test_get_history_invalid_symbol (negative)
#      - Make a GET request to /stocks/INVALID/history
#      - Assert the response status code is 404
#      - Assert the response contains an "error" field
#
#   3. test_get_history_no_auth_required (positive)
#      - Make a GET request to /stocks/MSFT/history WITHOUT an API key
#      - Assert the response status code is 200 (no auth needed)
#
# Hints:
# ------
# - Use the `requests` library to make HTTP requests
# - BASE_URL is already defined as "http://localhost:5000"
# - Run your tests with: pytest tests/functional/test_stock_history.py -v
# - Make sure the API server is running before executing the tests

import pytest
import requests

BASE_URL = "http://localhost:5000"


@pytest.mark.functional
class TestStockHistory:

    @pytest.mark.positive
    def test_get_stock_history(self):
        # TODO: Implement this test
        pass

    @pytest.mark.negative
    def test_get_history_invalid_symbol(self):
        # TODO: Implement this test
        pass

    @pytest.mark.positive
    def test_get_history_no_auth_required(self):
        # TODO: Implement this test
        pass
