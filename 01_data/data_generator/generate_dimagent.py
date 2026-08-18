"""Generate DimAgent (one row per agent) with referential integrity to FactSupportTicket.csv.

Emits exactly one row per distinct AgentKey found in the fact table, so every
FactSupportTicket.AgentKey resolves to one DimAgent row (1:M). Team, Team Lead, and
Operations Manager are assigned deterministically so rollups stay consistent.
"""
import csv
import os
import random
from datetime import date, timedelta

BASE = os.path.dirname(os.path.dirname(__file__))  # -> 01_data
FACT_PATH = os.path.join(BASE, "raw", "FactSupportTicket.csv")
OUT_PATH = os.path.join(BASE, "raw", "DimAgent.csv")

random.seed(42)

COLUMNS = [
    "AgentKey", "AgentID", "AgentName", "TeamName",
    "TeamLead", "OperationsManager", "HireDate", "IsActive",
]

# Teams -> (Team Lead, Operations Manager). Agents are spread across these teams.
TEAMS = [
    ("Team Aurora",   "Priya Nair",       "Marcus Webb"),
    ("Team Borealis", "Diego Alvarez",    "Marcus Webb"),
    ("Team Cascade",  "Hannah Schmidt",   "Rachel Osei"),
    ("Team Delta",    "Kenji Tanaka",     "Rachel Osei"),
    ("Team Everest",  "Fatima Al-Sayed",  "Thomas Nguyen"),
]

FIRST_NAMES = [
    "Liam", "Olivia", "Noah", "Emma", "Ava", "Ethan", "Sophia", "Mason", "Isabella",
    "Lucas", "Mia", "Amir", "Zara", "Chen", "Wei", "Aisha", "Carlos", "Nadia",
    "Ibrahim", "Elena", "Yuki", "Sofia", "Omar", "Leila", "Andre", "Grace",
    "Tariq", "Ingrid", "Rohan", "Maya", "Sven", "Priscilla", "Malik", "Anya",
    "Diego", "Freya", "Hassan", "Lucia", "Kofi", "Nina", "Pedro", "Sana",
    "Viktor", "Rania", "Jamal", "Beatriz", "Kai", "Amara", "Luka", "Farah",
]
LAST_NAMES = [
    "Smith", "Johnson", "Garcia", "Martinez", "Lee", "Brown", "Davis", "Lopez",
    "Wilson", "Anderson", "Thomas", "Khan", "Patel", "Nguyen", "Kim", "Chen",
    "Ali", "Silva", "Rossi", "Muller", "Haddad", "Okafor", "Sato", "Ivanov",
    "Costa", "Reyes", "Dubois", "Bauer", "Yilmaz", "Novak", "Popov", "Mensah",
    "Abbas", "Fernandez", "Petrov", "Larsson", "Tran", "Osei", "Cruz", "Berg",
    "Hansen", "Moreau", "Kaur", "Adeyemi", "Vasquez", "Weber", "Park", "Diallo",
    "Romano", "Bianchi",
]


def distinct_agent_keys():
    keys = set()
    with open(FACT_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            keys.add(int(row["AgentKey"]))
    return sorted(keys)


def main():
    keys = distinct_agent_keys()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    used_names = set()
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)

        for key in keys:
            # Unique-ish full name
            while True:
                name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
                if name not in used_names:
                    used_names.add(name)
                    break

            team_name, team_lead, ops_manager = TEAMS[key % len(TEAMS)]

            # Hire date between 2019-01-01 and 2025-06-30
            hire = date(2019, 1, 1) + timedelta(days=random.randint(0, 2372))

            # ~90% active
            is_active = 1 if random.random() < 0.90 else 0

            writer.writerow([
                key,
                f"AG-{200 + key}",
                name,
                team_name,
                team_lead,
                ops_manager,
                hire.isoformat(),
                is_active,
            ])

    print(f"Wrote {len(keys)} agents -> {OUT_PATH}")


if __name__ == "__main__":
    main()
