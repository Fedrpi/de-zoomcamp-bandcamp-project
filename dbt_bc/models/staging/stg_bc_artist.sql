{{
  config(
    materialized = 'view',
    )
}}
select 
    id
   ,name
   ,case 
      when genre_tag is not Null then ARRAY_REVERSE(SPLIT(genre_tag, '/'))[SAFE_OFFSET(0)]
      else Null
    end genre
from {{ source('staging', 'artist') }}
{% if var('is_test_run', default=true) %}
limit 1000
{% endif %}