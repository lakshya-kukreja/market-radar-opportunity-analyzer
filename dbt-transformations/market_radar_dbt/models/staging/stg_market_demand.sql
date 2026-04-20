{{ config(
    materialized='view'
) }}

WITH source AS (
    SELECT * FROM {{ source('demand_source', 'raw_demand') }}
)

SELECT
    CAST(timestamp AS TIMESTAMP) AS event_timestamp,
    LOWER(CAST(city AS STRING)) AS city_name,
    LOWER(CAST(search_term AS STRING)) AS business_category,
    CAST(search_volume AS INT64) AS search_volume,
    CAST(sentiment_score AS FLOAT64) AS sentiment_score
FROM source
WHERE city IS NOT NULL