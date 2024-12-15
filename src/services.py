import datetime
import math
from datetime import datetime
from typing import Any, Dict, Hashable, List

from src.reading_excel_file import reading_excel


def profitable_cashback_categories(data, year, month):
    pass


def investment_bank(month: str, transactions: List[Dict[Hashable, Any]], limit: int) -> float:
    """Функция возвращает сумму, которую удалось бы отложить в Инвесткопилку"""
    if not datetime.strptime(month, "%Y-%m"):
        raise ValueError("Месяц указан в некорректном формате")

    if not isinstance(month, str) or not isinstance(transactions, list) or not isinstance(limit, int):
        raise TypeError("Неверный тип входных данных")

    transactions_for_month = []
    for transaction in transactions:
        date_obj = datetime.strptime(transaction.get("Дата операции"), "%d.%m.%Y %H:%M:%S")
        month_trans = str(date_obj.year) + "-" + str(date_obj.month)
        if month_trans == month:
            transactions_for_month.append(transaction)

    sum_for_invest = 0.0
    for transaction in transactions_for_month:
        sum_of_operation = str(transaction.get("Сумма операции"))
        if sum_of_operation[0] == "-":
            sum_for_invest += math.ceil(float(sum_of_operation[1:]) / float(limit)) * limit - float(
                sum_of_operation[1:]
            )
    return round(sum_for_invest, 2)


trans = reading_excel("../data/operations.xlsx")
print(investment_bank("2021-12", trans, 50))
