{{ config(materialized='table') }}

WITH supply AS (
    SELECT 
        TRIM(LOWER(city_name)) AS city_name, 
        TRIM(LOWER(business_type)) AS business_category, 
        SUM(existing_count) AS total_supply
    FROM {{ ref('fct_market_supply') }}
    GROUP BY 1, 2
),

demand AS (
    SELECT
        TRIM(LOWER(city_name)) AS city_name,
        TRIM(LOWER(business_category)) AS business_category,
        SUM(search_volume) AS total_demand,
        ROUND(AVG(sentiment_score), 2) AS avg_sentiment
    FROM {{ ref('fct_market_demand') }}
    GROUP BY 1, 2
)

SELECT
    d.city_name,
    d.business_category,
    COALESCE(s.total_supply, 0) AS current_supply,
    d.total_demand,
    d.avg_sentiment,
    ROUND(SAFE_DIVIDE(d.total_demand, COALESCE(s.total_supply, 1)), 2) AS opportunity_score
FROM demand d
LEFT JOIN supply s
  ON d.city_name = s.city_name
  AND d.business_category = s.business_category
ORDER BY opportunity_score DESC