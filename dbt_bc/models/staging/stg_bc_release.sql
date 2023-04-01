{{
  config(
    materialized = 'view',
    )
}}
select 
    album_id
   ,id
   ,name
   ,format
   ,price
   ,currency
   ,availability
   ,case
      when id like '%merch%' then 'merch'
      else 'music'
    end release_type
from {{ source('staging', 'release') }}
{% if var('is_test_run', default=true) %}
limit 1000
{% endif %}