from unittest.mock import patch

import pytest

from src.reading_excel_file import reading_excel


@patch("pandas.read_excel")
def test_reading_excel(mock_read_excel):
    mock_read_excel.return_value.to_dict.return_value = [
        {
            "Дата операции": "31.12.2021 16:44:00",
            "Дата платежа": "31.12.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": "-160,89",
        }
    ]
    assert reading_excel("test_file.excel") == [
        {
            "Дата операции": "31.12.2021 16:44:00",
            "Дата платежа": "31.12.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": "-160,89",
        }
    ]


@patch("pandas.read_excel", side_effect=FileNotFoundError)
def test_reading_excel_file_not_found(mock_file):
    try_to_read_excel = reading_excel("test_file.excel")
    assert try_to_read_excel == []


def test_reading_excel_wrong_input_data():
    with pytest.raises(TypeError):
        reading_excel(1, 2)
    with pytest.raises(TypeError):
        reading_excel([1, 2])
