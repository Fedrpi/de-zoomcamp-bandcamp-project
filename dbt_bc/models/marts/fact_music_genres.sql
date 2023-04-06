{{
  config(
    materialized = 'table',
    )
}}
with albums as (
  select
    artist_id
   ,id
  from {{ ref("stg_bc_album") }} 
),

artists as (
  select 
    id
   ,genre
   from {{ ref("stg_bc_artist") }}
    where genre is not null
),

tracks as (
  select
    album_id
   ,duration
  from {{ ref('stg_bc_track') }}
),

merch as (
  select
    album_id
   ,id
  from {{ ref("stg_bc_release") }}
  where release_type = 'merch'
),

df as (
  select 
    ar.genre
   ,ar.id artist_id
   ,al.id album_id
   ,tr.duration
   ,m.id merch_id
  from artists ar
  left join albums al
         on ar.id = al.artist_id
  left join tracks tr
         on al.id = tr.album_id
  left join merch m
         on al.id = m.album_id 
),

result as (
  select
    genre
   ,count(distinct artist_id) total_artists
   ,count(distinct album_id) total_albums
   ,avg(duration) song_mean_duraton
   ,count(distinct merch_id) total_merch
  from df
  group by 1
)

select * from result