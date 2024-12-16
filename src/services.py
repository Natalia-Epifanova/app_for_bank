import json
import logging
import math
import re
from datetime import datetime
from typing import Any, Dict, Hashable, List, final

import pandas as pd

from src.reading_excel_file import reading_excel

logger = logging.getLogger("services")
file_handler = logging.FileHandler("../logs/services.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def profitable_cashback_categories(transactions: List[Dict[Hashable, Any]], year, month) -> str:
    """Функция считает, какие были более выгодные категории кешбека в выбранном месяце"""
    logger.info("Начало работы функции для поиска более выгодных категорий кешбека")
    if not isinstance(month, str) or not isinstance(transactions, list) or not isinstance(year, str):
        logger.error("Неверный тип входных данных")
        raise TypeError("Неверный тип входных данных")
    transactions_for_month = []
    logger.info("Поиск транзакций за заданный месяц в списке транзакций")
    for transaction in transactions:
        date_obj = datetime.strptime(str(transaction.get("Дата операции")), "%d.%m.%Y %H:%M:%S")
        month_trans = str(date_obj.year) + "-" + str(date_obj.month)
        if month_trans == (year + "-" + month):
            transactions_for_month.append(transaction)
    logger.info("Обработка всех оплат за заданный месяц")

    df = pd.DataFrame(transactions_for_month)
    logger.info("Группировка оп категориям кэшбэка")
    result = df.groupby("Категория")["Кэшбэк"].sum()
    logger.info("Сортировка кэшбэка по убыванию")
    result = result.sort_values(ascending=False)
    result_dict = result.to_dict()

    final_result = {}
    for key, value in result_dict.items():

        if value > 0:
            final_result[key] = value
    logger.info("Функция отработала успешно!")
    return json.dumps(final_result, ensure_ascii=False, indent=4)


def investment_bank(month: str, transactions: List[Dict[Hashable, Any]], limit: int) -> float:
    """Функция возвращает сумму, которую удалось бы отложить в Инвесткопилку"""
    logger.info("Начало работы функции Инвесткопилка")
    if not datetime.strptime(month, "%Y-%m"):
        logger.error("Месяц указан в некорректном формате")
        raise ValueError("Месяц указан в некорректном формате")

    if not isinstance(month, str) or not isinstance(transactions, list) or not isinstance(limit, int):
        logger.error("Неверный тип входных данных")
        raise TypeError("Неверный тип входных данных")

    transactions_for_month = []
    logger.info("Поиск транзакций за заданный месяц в списке транзакций")
    for transaction in transactions:
        date_obj = datetime.strptime(str(transaction.get("Дата операции")), "%d.%m.%Y %H:%M:%S")
        month_trans = str(date_obj.year) + "-" + str(date_obj.month)
        if month_trans == month:
            transactions_for_month.append(transaction)

    sum_for_invest = 0.0
    if transactions_for_month:
        logger.info("Обработка всех оплат за заданный месяц")
        for transaction in transactions_for_month:
            sum_of_operation = str(transaction.get("Сумма операции"))
            if sum_of_operation[0] == "-":
                sum_for_invest += math.ceil(float(sum_of_operation[1:]) / float(limit)) * limit - float(
                    sum_of_operation[1:]
                )
    logger.info("Функция отработала успешно!")
    return round(sum_for_invest, 2)


def search_by_string(transactions: List[Dict[Hashable, Any]], string_for_search: str) -> str:
    """Функция возвращает список словарей с транзакциями, у которых в описании есть необходимая слово/строка"""
    logger.info("Начало работы функции для поиска по строке")
    if not isinstance(transactions, list) or not isinstance(string_for_search, str):
        logger.error("Неверный тип входных данных")
        raise TypeError("Неверный тип входных данных")
    pattern = rf"{string_for_search}"
    result_list = []
    logger.info("Поиск необходимой строки в категориях и описаниях транзакций")
    for transaction in transactions:
        if re.findall(pattern, str(transaction["Категория"]), flags=re.IGNORECASE):
            result_list.append(transaction)
        elif re.findall(pattern, str(transaction["Описание"]), flags=re.IGNORECASE):
            result_list.append(transaction)
    logger.info("Перевод полученных данных в JSON ответ")
    json_data = json.dumps(result_list, ensure_ascii=False, indent=4)
    logger.info("Функция отработала успешно!")
    return json_data


def search_by_phone(transactions: List[Dict[Hashable, Any]]) -> str:
    """Функция осуществляет поиск среди операций по телефонным номерам"""
    logger.info("Начало работы функции для поиска по номеру телефона")
    if not isinstance(transactions, list):
        logger.error("Неверный тип входных данных")
        raise TypeError("Неверный тип входных данных")

    pattern = re.compile(r"\d\s\d{3}\s\d{3}-\d{2}-\d{2}")
    new_transactions_list = []
    logger.info("Поиск в словаре транзакций операций по мобильной связи")
    for transaction in transactions:
        if re.findall(pattern, str(transaction["Описание"])):
            new_transactions_list.append(transaction)
    json_data = json.dumps(new_transactions_list, ensure_ascii=False, indent=4)
    logger.info("Функция отработала успешно!")
    return json_data


def search_by_transfers_to_individuals(transactions: List[Dict[Hashable, Any]]) -> str:
    """Функция осуществляет поиск переводов физическим лицам"""
    logger.info("Начало работы функции для поиска переводов физическим лицам")
    if not isinstance(transactions, list):
        logger.error("Неверный тип входных данных")
        raise TypeError("Неверный тип входных данных")

    pattern = re.compile(r"^[А-Яа-я]+\s[А-Я]\.$")
    new_transactions_list = []
    logger.info("Поиск в словаре транзакций переводов физическим лицам")
    for transaction in transactions:
        if (str(transaction["Категория"]) == "Переводы") and (re.findall(pattern, str(transaction["Описание"]))):
            new_transactions_list.append(transaction)
    json_data = json.dumps(new_transactions_list, ensure_ascii=False, indent=4)
    logger.info("Функция отработала успешно!")
    return json_data


trans = reading_excel("../data/operations.xlsx")
# print(investment_bank("2021-12", trans, 50))
# print(search_by_string(trans, 'Каршеринг'))
# print(profitable_cashback_categories(trans, "2021", "3"))
# (search_by_phone(trans))
print(search_by_transfers_to_individuals(trans))
