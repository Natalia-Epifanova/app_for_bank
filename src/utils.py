import datetime
from datetime import datetime
from typing import Any, Dict, Hashable, List
import pandas as pd
from src.reading_excel_file import reading_excel
import json


def get_real_time_for_greetings() -> str:
    """Функция возвращает «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
    в зависимости от текущего времени."""
    current_date_time = datetime.datetime.now()
    if 6 <= current_date_time.hour <= 11:
        return "Доброе утро"
    elif 11 < current_date_time.hour <= 17:
        return "Добрый день"
    elif 17 < current_date_time.hour <= 21:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def search_transactions_for_month(
    originals_transactions: List[Dict[Hashable, Any]], date_time: str
) -> List[Dict[Hashable, Any]]:
    """Функция оставляет только транзакции за нужный месяц"""
    date_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    transactions_for_month = []
    if originals_transactions:
        for transaction in originals_transactions:
            date_obj_trans = datetime.strptime(str(transaction.get("Дата операции")), "%d.%m.%Y %H:%M:%S")
            if (
                date_obj_trans.month == date_obj.month
                and date_obj_trans.day <= date_obj.day
                and date_obj_trans.year == date_obj.year
            ):
                transactions_for_month.append(transaction)
    return transactions_for_month


def cards_information(transactions: List[Dict[Hashable, Any]]) -> str | None:
    """Функция возвращает расходы и кэшбеки по всей карте за месяц"""
    df = pd.DataFrame(transactions)
    result = df.groupby("Номер карты").agg({"Сумма операции": "sum", "Кэшбэк": "sum"})

    result_dict = result.to_dict()
    result = []
    for card_number, values in result_dict["Сумма операции"].items():
        card = {
            "last_digits": card_number[1:],
            "total_spent": abs(values),
            "cashback": result_dict["Кэшбэк"][card_number],
        }
        result.append(card)
    return json.dumps(result, ensure_ascii=False, indent=4)


trans = reading_excel("../data/operations.xlsx")
print(cards_information(search_transactions_for_month(trans, "2021-12-01 10:20:47")))
