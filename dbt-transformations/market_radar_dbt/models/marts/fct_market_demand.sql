{{ config(
    materialized='table',
    partition_by={
      "field": "event_timestamp",
      "data_type": "timestamp",
      "granularity": "day"
    }
) }}

WITH raw_demand AS (
    SELECT * FROM {{ ref('stg_market_demand') }}
)

SELECT
    event_timestamp,
    city_name,
    business_category,
    search_volume,
    sentiment_score
FROM raw_demand