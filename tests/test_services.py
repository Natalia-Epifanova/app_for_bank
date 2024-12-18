import json

import pytest

from src.services import (
    investment_bank,
    profitable_cashback_categories,
    search_by_phone,
    search_by_string,
    search_by_transfers_to_individuals,
)


def test_search_by_string_description(transactions_for_test):
    result = search_by_string(transactions_for_test, "Каршеринг")
    expected_result = [
        {
            "Дата операции": "28.12.2021 18:42:21",
            "Дата платежа": "28.12.2021",
            "Номер карты": "*7197",
            "Сумма операции": -257.9,
            "Кэшбэк": 20,
            "Категория": "Каршеринг",
            "Описание": "Ситидрайв",
        }
    ]
    assert json.loads(result) == expected_result


def test_search_by_string_category(transactions_for_test):
    result = search_by_string(transactions_for_test, "Колхоз")
    expected_result = [
        {
            "Дата операции": "31.12.2021 16:44:00",
            "Дата платежа": "31.12.2021",
            "Номер карты": "*7197",
            "Сумма операции": -160.9,
            "Кэшбэк": 70,
            "Категория": "Супермаркеты",
            "Описание": "Колхоз",
        }
    ]
    assert json.loads(result) == expected_result


def test_search_by_string_type_error():
    with pytest.raises(TypeError):
        search_by_string(123, "Каршеринг")
    with pytest.raises(TypeError):
        search_by_string([], 123)


def test_search_by_string_empty_list():
    result = search_by_string([], "Каршеринг")
    assert result is None


def test_search_by_string_missing_string():
    result = search_by_string([], "Яблоко")
    assert result is None


def test_search_by_phone(transactions_for_test):
    result = search_by_phone(transactions_for_test)
    expected_result = [
        {
            "Дата операции": "29.12.2021 22:28:47",
            "Дата платежа": "29.12.2021",
            "Номер карты": "*7197",
            "Сумма операции": -1411.4,
            "Кэшбэк": 0,
            "Категория": "Пополнения",
            "Описание": "Тинькофф Мобайл +7 995 555-55-55",
        }
    ]
    assert json.loads(result) == expected_result


def test_search_by_phone_type_error():
    with pytest.raises(TypeError):
        search_by_phone(123)


def test_search_by_phone_empty_list():
    result = search_by_phone([])
    assert result is None


def test_search_by_phone_no_transactions_with_phone(transactions_for_test_without_phone_num):
    result = search_by_phone(transactions_for_test_without_phone_num)
    assert result == "[]"


def test_search_by_transfers_to_individuals(transactions_for_test):
    result = search_by_transfers_to_individuals(transactions_for_test)
    expected_result = [
        {
            "Дата операции": "23.12.2021 16:14:59",
            "Дата платежа": "23.12.2021",
            "Номер карты": "*7197",
            "Сумма операции": -2000,
            "Кэшбэк": 0,
            "Категория": "Переводы",
            "Описание": "Дмитрий Ш.",
        }
    ]
    assert json.loads(result) == expected_result


def test_search_by_transfers_to_individuals_empty_list():
    result = search_by_transfers_to_individuals([])
    assert result is None


def test_search_by_transfers_to_individuals_type_error():
    with pytest.raises(TypeError):
        search_by_transfers_to_individuals(123)


def test_search_by_transfers_to_individuals_no_transfers_to_ind(transactions_for_test_without_transfers_to_ind):
    result = search_by_transfers_to_individuals(transactions_for_test_without_transfers_to_ind)
    assert result == "[]"


def test_investment_bank(transactions_for_test):
    result = investment_bank("2021-12", transactions_for_test, 50)
    assert result == 119.8


def test_investment_bank_empty_list():
    result = investment_bank("2021-12", [], 50)
    assert result is None


def test_investment_bank_type_error():
    with pytest.raises(TypeError):
        investment_bank(12, [], 10)
    with pytest.raises(TypeError):
        investment_bank("2021-12", [], "10")
    with pytest.raises(TypeError):
        investment_bank("2021-12", 123, 10)


def test_profitable_cashback_categories_type_error():
    with pytest.raises(TypeError):
        profitable_cashback_categories([], 2021, 5)
    with pytest.raises(TypeError):
        profitable_cashback_categories(123, "2021", 5)


def test_profitable_cashback_categories(transactions_for_test):
    result = profitable_cashback_categories(transactions_for_test, "2021", "12")
    expected_result = {"Супермаркеты": 70, "Каршеринг": 20}

    assert json.loads(result) == expected_result
