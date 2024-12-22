import json
from datetime import datetime
from unittest.mock import mock_open, patch

import pytest
from requests import RequestException

from src.utils import (cards_information, get_currency, get_real_time_for_greetings, get_stock_prices, json_currency,
                       json_stock_prices, search_transactions_for_month, top_transactions)


@patch("src.utils.datetime")
def test_get_real_time_for_greetings_morning(mock_datetime):
    mock_datetime.now.return_value = datetime(2022, 10, 31, 8, 0, 0)
    assert get_real_time_for_greetings() == "Доброе утро"


@patch("src.utils.datetime")
def test_get_real_time_for_greetings_day(mock_datetime):
    mock_datetime.now.return_value = datetime(2022, 10, 31, 12, 0, 0)
    assert get_real_time_for_greetings() == "Добрый день"


@patch("src.utils.datetime")
def test_get_real_time_for_greetings_evening(mock_datetime):
    mock_datetime.now.return_value = datetime(2022, 10, 31, 19, 0, 0)
    assert get_real_time_for_greetings() == "Добрый вечер"


@patch("src.utils.datetime")
def test_get_real_time_for_greetings_night(mock_datetime):
    mock_datetime.now.return_value = datetime(2022, 10, 31, 22, 0, 0)
    assert get_real_time_for_greetings() == "Доброй ночи"


def test_cards_information(transactions_for_test):
    result = cards_information(transactions_for_test)
    expected_result = [
        {
            "last_digits": "7197",
            "total_spent": 3830.2,
            "cashback": 38.3,
        }
    ]
    assert result == expected_result


@patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD"]}')
@patch("requests.get")
def test_get_currency_json_currency(mock_get, mock_file):
    mock_get.return_value.json.return_value = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 1},
        "info": {"timestamp": 1733231405, "rate": 105.945524},
        "date": "2024-12-03",
        "result": 104.5,
    }
    assert get_currency("USD") == 104.5
    answer_for_test = json_currency("../user_settings.json")
    assert answer_for_test == [
        {
            "currency": "USD",
            "rate": 104.5,
        }
    ]


@patch("requests.get", side_effect=RequestException)
def test_get_currency_request_exception(mock_get):
    result = get_currency("USD")
    assert result == 0.0


@patch("builtins.open", side_effect=FileNotFoundError)
def test_json_currency_error(mock_file):
    data_for_test = json_currency("data/test.json")
    assert data_for_test is None


@patch("builtins.open", side_effect=FileNotFoundError)
def test_json_stock_prices_error(mock_file):
    data_for_test = json_stock_prices("data/test.json")
    assert data_for_test is None


@patch("builtins.open", new_callable=mock_open, read_data='{"user_stocks": ["AAPL"]}')
@patch("requests.get")
def test_get_stock_prices_json_stock_prices(mock_get, mock_file):
    mock_get.return_value.json.return_value = {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "price": 253.48,
        "exchange": "NASDAQ",
        "updated": 1706302801,
        "currency": "USD",
    }
    assert get_stock_prices("AAPL") == 253.48
    answer_for_test = json_stock_prices("../user_settings.json")
    assert answer_for_test == [
        {
            "stock": "AAPL",
            "price": 253.48,
        }
    ]


@patch("requests.get", side_effect=RequestException)
def test_get_stock_prices_exception(mock_get):
    result = get_stock_prices("AAPL")
    assert result == 0.0


def test_search_transactions_for_month(transactions_for_test_filter_by_month):
    result = search_transactions_for_month(transactions_for_test_filter_by_month, "2021-11-25 10:20:47")
    expected_result = [
        {
            "Дата операции": "23.11.2021 16:14:59",
            "Дата платежа": "23.12.2021",
            "Номер карты": "*7197",
            "Сумма операции": -2000,
            "Кэшбэк": 0,
            "Категория": "Переводы",
            "Описание": "Дмитрий Ш.",
        }
    ]

    assert result == expected_result


def test_top_transactions(transactions_for_test_without_transfers_to_ind):
    result = top_transactions(transactions_for_test_without_transfers_to_ind)
    expected_result = [
        {
            "date": "28.12.2021",
            "amount": 257.89,
            "category": "Каршеринг",
            "description": "Ситидрайв",
        },
        {
            "date": "31.12.2021",
            "amount": 160.89,
            "category": "Супермаркеты",
            "description": "Колхоз",
        },
    ]

    assert result == expected_result
