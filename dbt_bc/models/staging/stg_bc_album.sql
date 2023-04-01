{{
  config(
    materialized = 'view',
    )
}}
select
    artist_id
   ,id
   ,name
   ,numTracks as num_tracks
   ,keywords
   ,{{ convert_date('datePublished') }} date_published
   ,{{ convert_date('dateModified') }} date_modified
from {{ source('staging', 'album') }}
{% if var('is_test_run', default=true) %}
limit 1000
{% endif %}