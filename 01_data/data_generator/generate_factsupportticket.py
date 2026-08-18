"""Generate dummy data for FactSupportTicket (10,000 rows) per the Data Dictionary."""
import csv
import os
import random
from datetime import datetime, timedelta

random.seed(42)

ROWS = 10_000
OUT_PATH = os.path.join(os.path.dirname(__file__), "raw", "FactSupportTicket.csv")

# Dimension cardinalities (consistent with the star schema in the Data Dictionary)
NUM_AGENTS = 50            # DimAgent.AgentKey -> 1..50
NUM_CLIENTS = 8            # DimClient.ClientKey -> 1..8
NUM_CHANNELS = 3           # DimChannel.ChannelKey -> 1..3 (Voice, Email, Chat)

# Date range for ticket creation
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2026, 8, 13)          # current date
DATE_SPAN_DAYS = (END_DATE - START_DATE).days

# Per-client SLA target hours (threshold behind SLA_Met)
CLIENT_SLA_TARGET_HOURS = {c: t for c, t in zip(range(1, NUM_CLIENTS + 1),
                                                [24, 48, 12, 36, 24, 72, 8, 48])}

COLUMNS = [
    "TicketKey", "TicketID", "DateKey", "AgentKey", "ClientKey", "ChannelKey",
    "CreatedDateTime", "ResolvedDateTime", "ResolutionHours", "IsResolved",
    "SLA_Met", "CSAT_Score",
]


def normal_csat():
    """CSAT 1-5, normally distributed (mean 4.0, std 0.9), ~15% no-response nulls."""
    if random.random() < 0.15:
        return ""  # customer did not respond
    score = round(random.gauss(4.0, 0.9))
    return max(1, min(5, score))


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)

        for ticket_key in range(1, ROWS + 1):
            client_key = random.randint(1, NUM_CLIENTS)
            channel_key = random.randint(1, NUM_CHANNELS)
            agent_key = random.randint(1, NUM_AGENTS)

            # Created datetime somewhere in the range
            created = START_DATE + timedelta(
                days=random.randint(0, DATE_SPAN_DAYS),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59),
            )
            date_key = int(created.strftime("%Y%m%d"))

            # 82% resolved, 18% still open (backlog)
            is_resolved = 1 if random.random() < 0.82 else 0

            if is_resolved:
                # Log-normal-ish resolution time, kept positive
                resolution_hours = round(abs(random.gauss(18, 12)) + 0.5, 2)
                resolved = created + timedelta(hours=resolution_hours)
                resolved_str = resolved.strftime("%Y-%m-%d %H:%M:%S")
                sla_target = CLIENT_SLA_TARGET_HOURS[client_key]
                sla_met = 1 if resolution_hours <= sla_target else 0
            else:
                resolution_hours = ""
                resolved_str = ""      # null while still open
                sla_met = 0            # not yet met while open

            writer.writerow([
                ticket_key,
                f"TCK-{10000 + ticket_key}",
                date_key,
                agent_key,
                client_key,
                channel_key,
                created.strftime("%Y-%m-%d %H:%M:%S"),
                resolved_str,
                resolution_hours,
                is_resolved,
                sla_met,
                normal_csat(),
            ])

    print(f"Wrote {ROWS} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
