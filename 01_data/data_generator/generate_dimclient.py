"""Generate DimClient (one row per client) with referential integrity to FactSupportTicket.csv.

Emits exactly one row per distinct ClientKey found in the fact table (1:M). SLA_TargetHours
matches the thresholds the fact generator used, so SLA_Met stays consistent with the dimension.
"""
import csv
import os
from datetime import date

BASE = os.path.dirname(os.path.dirname(__file__))  # -> 01_data
FACT_PATH = os.path.join(BASE, "raw", "FactSupportTicket.csv")
OUT_PATH = os.path.join(BASE, "raw", "DimClient.csv")

COLUMNS = [
    "ClientKey", "ClientName", "Industry", "Region",
    "SLA_TargetHours", "ContractStartDate", "IsActive",
]

# ClientKey -> attributes. SLA_TargetHours mirrors the fact generator's thresholds.
CLIENTS = {
    1: ("Client A", "Retail",  "North America", 24, "2022-03-01", 1),
    2: ("Client B", "Telecom", "Europe",        48, "2021-07-15", 1),
    3: ("Client C", "Retail",  "North America", 12, "2023-01-10", 1),
    4: ("Client D", "Telecom", "Asia Pacific",  36, "2020-11-05", 1),
    5: ("Client E", "Retail",  "Europe",        24, "2022-09-20", 1),
    6: ("Client F", "Telecom", "Latin America", 72, "2019-05-30", 1),
    7: ("Client G", "Retail",  "North America",  8, "2023-06-01", 1),
    8: ("Client H", "Telecom", "Asia Pacific",  48, "2021-02-14", 0),
}


def distinct_client_keys():
    keys = set()
    with open(FACT_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            keys.add(int(row["ClientKey"]))
    return sorted(keys)


def main():
    keys = distinct_client_keys()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)

        for key in keys:
            name, industry, region, sla, start, active = CLIENTS[key]
            writer.writerow([
                key,
                name,
                industry,
                region,
                f"{sla:.2f}",
                start,
                active,
            ])

    print(f"Wrote {len(keys)} clients -> {OUT_PATH}")


if __name__ == "__main__":
    main()
