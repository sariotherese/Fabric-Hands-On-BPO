"""Generate CSATSurveyResponse with referential integrity to FactSupportTicket.csv.

One optional survey per ticket (unique TicketKey), covering only resolved tickets where the
customer left a CSAT score. Numeric columns (sub-ratings, NPS, response time) are drawn from
normal distributions; sub-rating means are centered on the ticket's CSAT so feedback stays coherent.
"""
import csv
import os
import random
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.dirname(__file__))  # -> 01_data
FACT_PATH = os.path.join(BASE, "raw", "FactSupportTicket.csv")
OUT_PATH = os.path.join(BASE, "raw", "CSATSurveyResponse.csv")

random.seed(42)

# Share of eligible (resolved + CSAT given) tickets that complete the detailed survey.
SURVEY_COMPLETION_RATE = 0.75

COLUMNS = [
    "SurveyResponseKey", "TicketKey", "SurveyResponseDate",
    "AgentCourtesyRating", "ResolutionQualityRating", "WaitTimeRating",
    "FirstContactResolution", "NPS_Score", "CustomerComment", "ResponseTimeHours",
]

POSITIVE_COMMENTS = [
    "Agent was friendly and solved my issue quickly.",
    "Great service, very professional and helpful.",
    "Resolved on the first call, very satisfied.",
    "Polite and knowledgeable support, thank you.",
    "Quick response and clear explanation.",
]
NEUTRAL_COMMENTS = [
    "Issue was resolved but it took a while.",
    "Support was okay, nothing exceptional.",
    "Got what I needed eventually.",
    "Average experience overall.",
    "The agent was fine but I had to wait.",
]
NEGATIVE_COMMENTS = [
    "Waited far too long and the problem is still not fixed.",
    "Agent was not helpful and seemed rushed.",
    "Had to contact you multiple times for the same issue.",
    "Very frustrating experience, poor communication.",
    "The problem was not resolved and no follow-up.",
]


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


def normal_rating(mean):
    """1-5 rating, normally distributed around mean (std 0.8)."""
    return int(clamp(round(random.gauss(mean, 0.8)), 1, 5))


def pick_comment(csat):
    if csat >= 4:
        return random.choice(POSITIVE_COMMENTS)
    if csat == 3:
        return random.choice(NEUTRAL_COMMENTS)
    return random.choice(NEGATIVE_COMMENTS)


def load_eligible_tickets():
    """Resolved tickets that received a CSAT score, with their resolved timestamp."""
    rows = []
    with open(FACT_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["IsResolved"] == "1" and row["CSAT_Score"] not in ("", None) and row["ResolvedDateTime"]:
                rows.append((
                    int(row["TicketKey"]),
                    int(row["CSAT_Score"]),
                    datetime.strptime(row["ResolvedDateTime"], "%Y-%m-%d %H:%M:%S"),
                ))
    return rows


def main():
    eligible = load_eligible_tickets()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    survey_key = 0
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)

        for ticket_key, csat, resolved_dt in eligible:
            if random.random() > SURVEY_COMPLETION_RATE:
                continue  # customer did not complete the detailed survey

            survey_key += 1

            # Sub-ratings centered on the ticket's CSAT
            courtesy = normal_rating(csat + 0.3)
            resolution_quality = normal_rating(csat)
            wait_time = normal_rating(csat - 0.3)

            # First-contact resolution more likely when satisfaction is high
            fcr = 1 if random.random() < (0.35 + 0.12 * csat) else 0

            # NPS 0-10, normally distributed, mean scaled from CSAT
            nps = int(clamp(round(random.gauss(2 * csat - 2, 1.8)), 0, 10))

            # Response time in hours after closure, normally distributed and positive
            response_hours = round(abs(random.gauss(24, 18)) + 0.25, 2)
            survey_date = (resolved_dt + timedelta(hours=response_hours)).date()

            writer.writerow([
                survey_key,
                ticket_key,
                survey_date.isoformat(),
                courtesy,
                resolution_quality,
                wait_time,
                fcr,
                nps,
                pick_comment(csat),
                response_hours,
            ])

    print(f"Wrote {survey_key} survey responses -> {OUT_PATH}")


if __name__ == "__main__":
    main()
