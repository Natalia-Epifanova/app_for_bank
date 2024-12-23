import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, Hashable, List

import pandas as pd
import requests
from dotenv import load_dotenv


load_dotenv("../.env")
logger = logging.getLogger("utils")
file_handler = logging.FileHandler("../logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_real_time_for_greetings() -> str:
    """Функция возвращает «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
    в зависимости от текущего времени."""
    logger.info("Начало работы функции по возврату приветствия")
    current_date_time = datetime.now()
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
    logger.info("Начало работы функции по поиску транзакций за месяц")
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
    logger.info("Функции по поиску транзакций за месяц завершена")
    return transactions_for_month


def cards_information(transactions: List[Dict[Hashable, Any]]) -> list[dict[str, Any]] | None:
    """Функция возвращает расходы и кэшбеки по всей карте за месяц"""
    logger.info("Начало работы функции по возврату расходов и кэшбэков за месяц")
    df = pd.DataFrame(transactions)
    result = df.groupby("Номер карты")["Сумма операции"].sum()

    result_dict = result.to_dict()

    final_result = []
    for card_number, values in result_dict.items():
        card = {
            "last_digits": card_number[1:],
            "total_spent": round(abs(values), 2),
            "cashback": round(abs(values) / 100, 2),
        }
        final_result.append(card)
    logger.info("Функция по возврату расходов и кэшбэков за месяц отработала успешно")
    return final_result


def top_transactions(transactions: List[Dict[Hashable, Any]]) -> list[dict[str, Any]] | None:
    """Функция возвращает топ-5 транзакций по оплате за месяц"""
    logger.info("Начало работы функции по возврату топ-5 транзакций за месяц")
    df = pd.DataFrame(transactions)

    result = []
    top_transactions_df = df.nlargest(5, "Сумма операции с округлением")
    for transaction in top_transactions_df.to_dict(orient="records"):
        result.append(
            {
                "date": transaction["Дата операции"],
                "amount": transaction["Сумма операции с округлением"],
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
        )
    logger.info("Функция по возврату топ-5 транзакций за месяц отработала успешно")
    return result


def get_currency(currency: str) -> float:
    """Функция возвращает актуальные данные курса валют"""
    logger.info("Начало работы функции по возврату курса валют по API")
    try:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=" f"{currency}&amount=1"
        headers = {"apikey": os.getenv("API_KEY")}
        response = requests.get(url, headers=headers, data={}, allow_redirects=False)
        response.raise_for_status()
        logger.info("Функция по возврату актуальных данных курса валют отработала успешно")
        return round(float(response.json()["result"]), 2)
    except requests.exceptions.RequestException as ex:
        logger.error(f"Произошла ошибка: {ex}")
        print("An error occurred. Please try again later.")
    return 0.0


def json_currency(path: str) -> list[dict[str, Any]] | None:
    """Функция возвращает информацию о курсе валют, заданных в пользовательских настройках"""
    try:
        logger.info("Начало работы функции по возврату курса валют, заданных в пользовательских настройках")
        with open(path, encoding="UTF-8") as json_file:
            user_settings_data = json.load(json_file)
        final_result = []
        for element in user_settings_data["user_currencies"]:
            currency_info = {
                "currency": element,
                "rate": get_currency(element),
            }
            final_result.append(currency_info)
        logger.info("Функция по возврату курса валют, заданных в пользовательских настройках отработала успешно")
        return final_result
    except FileNotFoundError as ex:
        logger.error(f"Произошла ошибка: {ex}")
        return None


def get_stock_prices(company: str) -> float:
    """Функция возвращает актуальные данные по ценам акций"""
    try:
        logger.info("Начало работы функции по возврату цен акций по API")
        symbol = company
        api_url = "https://api.api-ninjas.com/v1/stockprice?ticker={}".format(symbol)
        headers = {"X-Api-Key": os.getenv("API_KEY_2")}
        response = requests.get(api_url, headers=headers)
        logger.info("Функция по возврату актуальных данных по ценам акций отработала успешно")
        return round(float(response.json()["price"]), 2)
    except requests.exceptions.RequestException as ex:
        logger.error(f"Произошла ошибка: {ex}")
        print("An error occurred. Please try again later.")
    return 0.0


def json_stock_prices(path: str) -> list[dict[str, Any]] | None:
    """Функция возвращает информацию о стоимости акций, заданных в пользовательских настройках"""
    try:
        logger.info(
            "Начало работы функции по возврату информации о стоимости акций, заданных в пользовательских настройках"
        )
        with open(path, encoding="UTF-8") as json_file:
            user_settings_data = json.load(json_file)
        final_result = []
        for element in user_settings_data["user_stocks"]:
            currency_info = {
                "stock": element,
                "price": get_stock_prices(element),
            }
            final_result.append(currency_info)
        logger.info(
            "Функция по возврату информации о стоимости акций, "
            "заданных в пользовательских настройках отработала успешно"
        )
        return final_result
    except FileNotFoundError as ex:
        logger.error(f"Произошла ошибка: {ex}")
        return None
