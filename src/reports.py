import json
import logging
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Hashable, List, Optional

import pandas as pd
from typing_extensions import final

from src.reading_excel_file import reading_excel

logger = logging.getLogger("reports")
file_handler = logging.FileHandler("../logs/reports.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def writing_data(file_name: str = "../data/reports.json") -> Callable:
    """Декоратор, который записывает в файл результат, возвращаемый функцией, формирующей отчет"""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            result.to_json(path_or_buf=file_name, orient="records", force_ascii=False, indent=4)
            return result

        return wrapper

    return decorator


@writing_data()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""
    logger.info("Начало работы функции, возвращающей траты по заданной категории за последние три месяца")
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    three_months_ago = date_obj - timedelta(days=90)
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")
    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (three_months_ago <= transactions["Дата платежа"])
        & (transactions["Дата платежа"] <= date)
    ]

    return filtered_transactions
