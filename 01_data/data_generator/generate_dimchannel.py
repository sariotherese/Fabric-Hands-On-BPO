"""Generate DimChannel (one row per contact channel) with referential integrity to FactSupportTicket.csv.

Emits exactly one row per distinct ChannelKey found in the fact table (1:M). Keys map to
Voice/Email/Chat, matching the channel ordering the fact generator used.
"""
import csv
import os

BASE = os.path.dirname(os.path.dirname(__file__))  # -> 01_data
FACT_PATH = os.path.join(BASE, "raw", "FactSupportTicket.csv")
OUT_PATH = os.path.join(BASE, "raw", "DimChannel.csv")

COLUMNS = ["ChannelKey", "ChannelName", "ChannelType", "TargetResponseMinutes", "IsActive"]

# ChannelKey -> (ChannelName, ChannelType, TargetResponseMinutes, IsActive)
CHANNELS = {
    1: ("Voice", "Real-time",    1,   1),
    2: ("Email", "Asynchronous", 240, 1),
    3: ("Chat",  "Real-time",    2,   1),
}


def distinct_channel_keys():
    keys = set()
    with open(FACT_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            keys.add(int(row["ChannelKey"]))
    return sorted(keys)


def main():
    keys = distinct_channel_keys()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
        for key in keys:
            name, ctype, target, active = CHANNELS[key]
            writer.writerow([key, name, ctype, target, active])

    print(f"Wrote {len(keys)} channels -> {OUT_PATH}")


if __name__ == "__main__":
    main()
