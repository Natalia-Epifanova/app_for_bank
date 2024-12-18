import pandas as pd
import json
from typing import Optional, Any, Dict, Hashable, List, Callable
from datetime import datetime, timedelta

from typing_extensions import final

from src.reading_excel_file import reading_excel


def writing_data(file_name: str = "reports.json") -> Callable:
    """Декоратор, который записывает в файл результат, возвращаемый функцией, формирующая отчет"""

    def decorator(func) -> Callable:
        def wrapper(*args, **kwargs) -> json:
            result = func(*args, **kwargs)
            result.to_json(path_or_buf=file_name, orient="records", force_ascii=False, indent=4)
            return result

        return wrapper

    return decorator



@writing_data()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца (от переданной даты)"""
    #logger.info("Ищем траты по конкретной категории")
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    three_months_ago = date_obj - timedelta(days=90)
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")
    filtered_transactions = transactions[
        (transactions["Категория"] == category) &
        (three_months_ago <= transactions["Дата платежа"]) &
        (transactions["Дата платежа"] <= date)
        ]
    return filtered_transactions

#
# def spending_by_weekday(transactions: pd.DataFrame,
#                         date: Optional[str] = None) -> pd.DataFrame:
#     if date is None:
#         date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
#     three_months_ago = date_obj - timedelta(days=90)
#     transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")
#     filtered_transactions = transactions[
#         (three_months_ago <= transactions["Дата платежа"]) &
#         (transactions["Дата платежа"] <= date)
#         ]
#     final_transactions = []
#     for index, row in filtered_transactions.iterrows():
#         date_payment = row["Дата платежа"]
#         print(date_payment, type(date_payment))
#         amount = row["Сумма платежа"]
#         date_payment = datetime.strptime(date_payment, "%d.%m.%Y")
#         weekday = date_payment.strftime(date_payment, '%A')
#         final_transactions.append({weekday: amount})
#     print(final_transactions)
#
#     #return filtered_transactions


trans = pd.DataFrame(reading_excel("../data/operations.xlsx"))
#print(spending_by_category(trans, 'Каршеринг', "2021-12-03 21:20:47"))
#print(search_transactions_for_three_months(trans, "2021-12-03 21:20:47"))
#print(spending_by_category(search_transactions_for_three_months(trans, "2021-12-03 21:20:47"), 'Каршеринг'))
#print(spending_by_weekday(search_transactions_for_three_months(trans, "2021-12-03 21:20:47")))
print(spending_by_weekday(trans, "2021-12-03 21:20:47"))