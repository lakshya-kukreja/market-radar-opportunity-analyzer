{{ config(
    materialized='table',
    partition_by={
      "field": "extraction_date",
      "data_type": "date",
      "granularity": "day"
    }
) }}

WITH staging_supply AS (
    SELECT * FROM {{ ref('stg_market_supply') }}
)

SELECT
    extraction_date,
    city_name,
    business_type,
    existing_count
FROM staging_supply