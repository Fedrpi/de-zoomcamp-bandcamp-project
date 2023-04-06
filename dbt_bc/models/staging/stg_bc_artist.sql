{{
  config(
    materialized = 'view',
    )
}}
select 
distinct
    id
   ,name
   ,case 
      when genre_tag is not Null then ARRAY_REVERSE(SPLIT(genre_tag, '/'))[SAFE_OFFSET(0)]
      else Null
    end genre
from {{ source('staging', 'artist') }}
where genre_tag is not null
{% if var('is_test_run', default=true) %}
limit 1000
{% endif %}