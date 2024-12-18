
import json
import os
from typing import Any, Dict, Hashable, List
from datetime import datetime
import pandas as pd
import requests
from dotenv import load_dotenv

from src.reading_excel_file import reading_excel

load_dotenv("../.env")


def get_real_time_for_greetings() -> str:
    """Функция возвращает «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
    в зависимости от текущего времени."""
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


def cards_information(transactions: List[Dict[Hashable, Any]]) -> list[dict[str, Any]] | None:
    """Функция возвращает расходы и кэшбеки по всей карте за месяц"""
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
    return final_result


def top_transactions(transactions: List[Dict[Hashable, Any]]) -> str | None:
    """Функция возвращает топ-5 транзакций по оплате за месяц"""
    df = pd.DataFrame(transactions)
    # df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    # #rez = df.groupby("Дата операции")["Сумма операции с округлением"].max()
    # df_grouped = df.groupby(df['Дата операции'].dt.date)['Сумма операции с округлением'].max().reset_index()
    # df_grouped_sorted = df_grouped.sort_values(by='Сумма операции с округлением', ascending=False)
    # df_dict = df_grouped_sorted.to_dict()
    # print(df_dict)
    # for index, item in enumerate(df_dict):
    #     print(df_dict[item])

    rez = df.sort_values(by="Сумма операции с округлением", ascending=False)
    top_5 = df.head(5)
    print(top_5)

    # # result = df.groupby("Дата операции")["Сумма операции с округлением"].max()
    # result_2 = df.sort_values(by='Сумма операции с округлением', ascending=False)
    # result_3 = result_2.to_dict()
    # result_4 = []
    # print(result_3)
    # for value in result_3:
    #     print(value)
    #     for value_2 in result_3[value].values():
    #         print(value_2)
    #         if value_2 in result_4:
    #             continue
    #         else:
    #             transaction = {
    #                 'date': value_2[0],
    #                 "amount": value_2[1],
    #                 "category": value_2[2],
    #                 "description": value_2[3]
    #             }
    #             result_4.append(transaction)
    #     print(result_4)


# {
#      "date": "20.12.2021",
#      "amount": 421.00,
#      "category": "Различные товары",
#      "description": "Ozon.ru"
#    },


def get_currency(currency: str) -> float:
    """Функция возвращает актуальные данные курса валют"""
    try:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=" f"{currency}&amount=1"
        headers = {"apikey": os.getenv("API_KEY")}
        response = requests.get(url, headers=headers, data={}, allow_redirects=False)
        response.raise_for_status()
        return round(float(response.json()["result"]), 2)
    except requests.exceptions.RequestException:
        print("An error occurred. Please try again later.")
    return 0.0


def json_currency() -> list[dict[str, Any]] | None:
    """Функция возвращает информацию о курсе валют, заданных в пользовательских настройках"""
    try:
        with open("../user_settings.json", encoding="UTF-8") as json_file:
            user_settings_data = json.load(json_file)
        final_result = []
        for element in user_settings_data["user_currencies"]:
            currency_info = {
                "currency": element,
                "rate": get_currency(element),
            }
            final_result.append(currency_info)
        return final_result
    except json.JSONDecodeError as ex:
        print("Invalid JSON data.")
        return None
    # logger.error(f"Произошла ошибка: {ex}")


def get_stock_prices(company: str) -> float:
    """Функция возвращает актуальные данные по ценам акций"""
    symbol = company
    api_url = "https://api.api-ninjas.com/v1/stockprice?ticker={}".format(symbol)
    headers = {"X-Api-Key": os.getenv("API_KEY_2")}
    response = requests.get(api_url, headers=headers)
    return round(float(response.json()["price"]), 2)


def json_stock_prices() -> list[dict[str, Any]] | None:
    """Функция возвращает информацию о стоимости акций, заданных в пользовательских настройках"""
    try:
        with open("../user_settings.json", encoding="UTF-8") as json_file:
            user_settings_data = json.load(json_file)
        final_result = []
        for element in user_settings_data["user_stocks"]:
            currency_info = {
                "stock": element,
                "price": get_stock_prices(element),
            }
            final_result.append(currency_info)
        return final_result
    except json.JSONDecodeError as ex:
        print("Invalid JSON data.")
        return None
    # logger.error(f"Произошла ошибка: {ex}")


trans = reading_excel("../data/operations.xlsx")
# print(top_transactions(search_transactions_for_month(trans, "2021-12-03 10:20:47")))
#print(get_stock_prices("AAPL"))
