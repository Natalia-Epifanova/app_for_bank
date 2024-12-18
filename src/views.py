from src.reading_excel_file import reading_excel
from src.utils import get_real_time_for_greetings, search_transactions_for_month, cards_information, json_currency, \
    json_stock_prices, top_transactions
import json


trans = reading_excel("../data/operations.xlsx")

def general_page(date_and_time: str) -> str | None:
    """Функция возвращает информацию о транзакциях за месяц, соответствующий дате, переданной пользователем"""
    greeting = get_real_time_for_greetings()
    transactions_for_month = search_transactions_for_month(trans, date_and_time)

    info_about_cards = cards_information(transactions_for_month)
    currencies = json_currency()
    stocks = json_stock_prices()

    final_result = {
        "greeting": greeting,
        "cards": info_about_cards,
        "top_transactions": [],
        "currency_rates": currencies,
        "stock_prices": stocks
    }
    print(final_result)
    return json.dumps(final_result, ensure_ascii=False, indent=4)

print(general_page("2021-12-29 10:20:47"))