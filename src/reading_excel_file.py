from typing import Any, Dict, Hashable, List

import pandas as pd

def reading_excel(path_to_excel: str) -> List[Dict[Hashable, Any]]:
    """Функция для считывания финансовых операций из XLSX файла"""
    if not isinstance(path_to_excel, str):
        raise TypeError("Неправильный формат пути к файлу")
    try:
        excel_file_df = pd.read_excel(path_to_excel)
        excel_reader = excel_file_df.to_dict(orient="records")
        return excel_reader
    except FileNotFoundError:
        return []

