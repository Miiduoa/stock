import csv


def load_closes(path):
    closes = []

    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)

        if "close" not in (reader.fieldnames or []):
            raise ValueError("CSV must contain a close column")

        for row in reader:
            closes.append(float(row["close"]))

    return closes
