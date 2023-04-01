{{
  config(
    materialized = 'view',
    )
}}
select 
    album_id
   ,id
   ,name
   ,case 
      when duration_sec is not Null then duration_sec / 60 
      else Null
    end duration
   ,position
from {{ source('staging', 'record') }}
{% if var('is_test_run', default=true) %}
limit 1000
{% endif %}