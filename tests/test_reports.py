from src.reports import spending_by_category, writing_data


def test_decorator_writing_data(transactions_data_frame):
    @writing_data()
    def my_function(transactions):
        return transactions

    my_function(transactions_data_frame)
    with open("../data/reports.json", "r", encoding="utf-8") as log_file:
        content = log_file.readlines()[3]
    assert content == '        "Дата платежа":"20.09.2021",\n'


def test_spending_by_category_no_data(transactions_data_frame):
    result_df = spending_by_category(transactions_data_frame, "Супермаркеты")
    assert len(result_df) == 0


def test_spending_by_category(transactions_data_frame):
    result_df = spending_by_category(transactions_data_frame, "Супермаркеты", "2021-11-15 12:00:00")
    assert len(result_df) == 2
