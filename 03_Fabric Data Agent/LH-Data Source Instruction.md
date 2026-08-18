# Lakehouse Data Source Instruction

## Scope

This Lakehouse contains only the `CSATSurveyResponse` table. Each row is one completed customer survey. Use it for survey details, comments, ad-hoc aggregations, response dates, courtesy, resolution quality, wait time, first-contact resolution, NPS, and response time.

## Source Selection

- Prefer the ontology for business concepts, standard metrics, and relationships involving tickets, agents, teams, clients, channels, and dates.
- Use the Lakehouse for survey-level detail, comments, ad-hoc aggregations, or survey fields not available in the ontology.
- Do not use the Lakehouse alone for ticket volume, backlog, SLA compliance, resolution time, or ticket-related attributes.
- When a question needs both sources, connect `CSATSurveyResponse.TicketKey` in the Lakehouse to the ticket `TicketKey` in the ontology. Use the ontology for business context and the Lakehouse for survey detail.

## Calculation Rules

- Use `SurveyResponseDate` when filtering by survey response date.
- Calculate metrics only from valid responses. Never treat missing surveys as zero or negative.
- FCR rate is the percentage of valid responses where `FirstContactResolution = 1`.
- NPS is the percentage of promoters (`NPS_Score` 9–10) minus detractors (`NPS_Score` 0–6); scores 7–8 are passive.
- Keep courtesy, resolution quality, and wait-time ratings as separate 1–5 measures unless the user requests a combined score.
- Include the response count with averages, percentages, rankings, and comparisons.

## Response Guidance

Keep answers concise. State the date range, filters, metric, and response count. Make clear that results cover survey respondents only, and do not claim they represent all customers without a valid response-rate analysis.