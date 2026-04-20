{{ config(
    materialized='view'
) }}

WITH raw_supply AS (
    SELECT * FROM {{ source('supply_source', 'supply_external') }}
    -- Note: Ensure you add 'supply_external' to your schema.yml sources!
)

SELECT
    CAST(extraction_date AS DATE) AS extraction_date,
    CAST(city AS STRING) AS city_name,
    CAST(business_type AS STRING) AS business_type,
    CAST(existing_count AS INT64) AS existing_count
FROM raw_supply
WHERE city IS NOT NULL 
AND business_type IS NOT NULL