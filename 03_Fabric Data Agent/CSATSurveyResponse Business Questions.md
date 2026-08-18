# CSATSurveyResponse Business Questions

The `CSATSurveyResponse` table contains 5,241 completed survey responses dated January 2, 2025 through August 16, 2026. Each result below represents survey respondents only. The queries use only this Lakehouse table and assume it is available as `CSATSurveyResponse` in the Fabric SQL analytics endpoint.

## 1. How did courtesy, resolution quality, and wait-time ratings trend by month in 2026?

```sql
SELECT
    YEAR(SurveyResponseDate) AS SurveyYear,
    MONTH(SurveyResponseDate) AS SurveyMonth,
    COUNT(*) AS ResponseCount,
    ROUND(AVG(CAST(AgentCourtesyRating AS DECIMAL(10, 2))), 2) AS AvgCourtesyRating,
    ROUND(AVG(CAST(ResolutionQualityRating AS DECIMAL(10, 2))), 2) AS AvgResolutionQualityRating,
    ROUND(AVG(CAST(WaitTimeRating AS DECIMAL(10, 2))), 2) AS AvgWaitTimeRating
FROM gold_db.CSATSurveyResponse
WHERE SurveyResponseDate >= '2026-01-01'
  AND SurveyResponseDate < '2027-01-01'
GROUP BY
    YEAR(SurveyResponseDate),
    MONTH(SurveyResponseDate)
ORDER BY
    SurveyYear,
    SurveyMonth;
```

## 2. What was the survey-reported first-contact resolution rate by month in 2026?

```sql
SELECT
    YEAR(SurveyResponseDate) AS SurveyYear,
    MONTH(SurveyResponseDate) AS SurveyMonth,
    COUNT(*) AS ResponseCount,
    ROUND(
        100.0 * SUM(CASE WHEN FirstContactResolution = 1 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        1
    ) AS FCRRatePercent
FROM gold_db.CSATSurveyResponse
WHERE SurveyResponseDate >= '2026-01-01'
  AND SurveyResponseDate < '2027-01-01'
GROUP BY
    YEAR(SurveyResponseDate),
    MONTH(SurveyResponseDate)
ORDER BY
    SurveyYear,
    SurveyMonth;
```

## 3. What was the Net Promoter Score by month in 2026?

```sql
SELECT
    YEAR(SurveyResponseDate) AS SurveyYear,
    MONTH(SurveyResponseDate) AS SurveyMonth,
    COUNT(*) AS ResponseCount,
    ROUND(
        100.0 * (
            SUM(CASE WHEN NPS_Score BETWEEN 9 AND 10 THEN 1 ELSE 0 END)
            - SUM(CASE WHEN NPS_Score BETWEEN 0 AND 6 THEN 1 ELSE 0 END)
        ) / NULLIF(COUNT(*), 0),
        1
    ) AS NPS
FROM gold_db.CSATSurveyResponse
WHERE SurveyResponseDate >= '2026-01-01'
  AND SurveyResponseDate < '2027-01-01'
GROUP BY
    YEAR(SurveyResponseDate),
    MONTH(SurveyResponseDate)
ORDER BY
    SurveyYear,
    SurveyMonth;
```

NPS classifies scores 9–10 as promoters, 7–8 as passives, and 0–6 as detractors. It is reported on a scale from -100 to 100.