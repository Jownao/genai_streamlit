{{ config(materialized='view') }}

WITH cleaned_data AS (
    SELECT 
        email, 
        DATE(data) AS data,
        valor, 
        quantidade, 
        produto
    FROM 
        {{ ref('bronze_vendas') }}
    WHERE 
        valor > 1000 
        AND valor < 8000
)

SELECT * FROM cleaned_data