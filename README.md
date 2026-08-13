# Fabric Data Agent Workshop

A hands-on workshop for building a **Microsoft Fabric Data Agent** — from setup and onboarding to asking questions of your data in plain English.

**Prepared by:** Therese Sario · Solutions Engineer, Microsoft Philippines

---

## Contents

- [Workshop Goal](#workshop-goal)
- [Business Scenario](#business-scenario)
  - [Company Overview](#company-overview)
  - [Business Requirement](#business-requirement)
  - [The Challenge](#the-challenge)
  - [The Solution](#the-solution)
- [Prerequisites](#prerequisites)
- [Repository Contents](#repository-contents)

---

## Workshop Goal

By the end of this session, attendees will be able to:

- Understand the **benefits** of a Fabric Data Agent
- **Set up and onboard** a Data Agent against their own data
- **Build a Fabric Data Agent independently** after the workshop

The session is built around the business scenario below.

---

## Business Scenario

### Company Overview

**Contoso Connect Solutions, Inc.** — a mid-sized Philippine **BPO** providing outsourced customer support (voice, email, chat) for international retail and telecom clients. Its 24/7 contact center runs **~400 agents** in Team Lead–led teams, with every interaction logged as a **support ticket**.

### Business Requirement

Operations Managers and Team Leads need to monitor daily contact-center performance:

- **Ticket volumes**
- **Resolution times** and backlog
- **Customer satisfaction (CSAT)**

This lets them staff shifts correctly, coach agents, and report **SLA compliance** to each client — with answers available **on demand and in plain English**, without waiting on the analytics team.

### The Challenge

All ticket data sits in a single operational table, but the people who need insights can't get to it quickly:

- **Reporting is a bottleneck.** Every new question — *"Which agents had the lowest CSAT this week?"*, *"How many tickets breached SLA yesterday for Client A?"* — becomes a request to a small BI/analyst team. Turnaround is often **1–2 days**.
- **Supervisors aren't technical.** Team Leads don't know SQL, DAX, or how to build a Power BI report, so they can't self-serve — even for simple lookups.
- **Decisions are delayed.** By the time a report arrives, the shift or coaching moment has passed, and **SLA breaches are caught after the fact** instead of being prevented.

### The Solution

A **Fabric Data Agent** built on the ticket data lets any supervisor ask questions in natural language and get instant, data-grounded answers — no SQL, no report-building, no waiting on analysts. Supervisors self-serve in **seconds instead of days**, and the analytics team is freed from routine ad-hoc requests.

---

## Prerequisites

- A **Microsoft Fabric** workspace (Fabric capacity or Trial)
- **Contributor** or higher permissions in the workspace
- Basic familiarity with the Fabric portal *(no coding required)*

---

## Repository Contents

| File | Description |
|------|-------------|
| `README.md` | This overview |
| _(add your lab files here)_ | Step-by-step lab guide, sample dataset, SQL scripts |
