"""Generate DimDate (one row per calendar day) with referential integrity to FactSupportTicket.csv.

Builds a continuous daily calendar spanning the min..max DateKey found in the fact table,
so every FactSupportTicket.DateKey resolves to exactly one DimDate row (1:M).
"""
import csv
import os
from datetime import datetime, timedelta

BASE = os.path.dirname(__file__)
FACT_PATH = os.path.join(BASE, "raw", "FactSupportTicket.csv")
OUT_PATH = os.path.join(BASE, "raw", "DimDate.csv")

COLUMNS = [
    "DateKey", "FullDate", "DayOfWeek", "WeekOfYear",
    "MonthNumber", "MonthName", "Quarter", "Year", "IsWeekend",
]


def fact_date_range():
    keys = []
    with open(FACT_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            keys.append(int(row["DateKey"]))
    lo, hi = min(keys), max(keys)
    return datetime.strptime(str(lo), "%Y%m%d"), datetime.strptime(str(hi), "%Y%m%d")


def main():
    start, end = fact_date_range()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)

        current = start
        while current <= end:
            writer.writerow([
                int(current.strftime("%Y%m%d")),
                current.strftime("%Y-%m-%d"),
                current.strftime("%A"),
                current.isocalendar().week,
                current.month,
                current.strftime("%B"),
                (current.month - 1) // 3 + 1,
                current.year,
                1 if current.weekday() >= 5 else 0,
            ])
            current += timedelta(days=1)

    print(f"Wrote DimDate from {start:%Y-%m-%d} to {end:%Y-%m-%d} -> {OUT_PATH}")


if __name__ == "__main__":
    main()
