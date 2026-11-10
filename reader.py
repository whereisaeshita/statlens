import csv
from pathlib import Path
from typing import Dict, List, Union


def read_csv_columns(file_path: Union[str, Path]) -> Dict[str, List[float]]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    columns: Dict[str, List[float]] = {}

    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return {}

        headers = [h.strip() or f"col_{i+1}" for i, h in enumerate(header)]
        for h in headers:
            columns[h] = []

        for row in reader:
            if not row or not any(row):
                continue
            for i, val in enumerate(row):
                if i >= len(headers):
                    break
                val_clean = val.strip()
                try:
                    num = float(val_clean)
                    columns[headers[i]].append(num)
                except ValueError:
                    pass

    return {col: vals for col, vals in columns.items() if vals}


def parse_numeric_string(raw_text: str) -> List[float]:
    delimiters = [",", "\n", "\t", " "]
    cleaned = raw_text
    for d in delimiters[1:]:
        cleaned = cleaned.replace(d, ",")

    tokens = cleaned.split(",")
    numbers = []
    for token in tokens:
        stripped = token.strip()
        if not stripped:
            continue
        try:
            numbers.append(float(stripped))
        except ValueError:
            pass
    return numbers

