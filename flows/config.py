import pyarrow as pa

artist_schema = {
    'id': ['@id'],
    'type': ['@type'],
    'name': ['name'],
    'genre_tag': ['genre'],
    'description': ['description'],
    'image': ['image'],
    'platforms_links': ['sameAs']
}

artist_schema_parquet = pa.schema([
    pa.field("id", pa.string(), True),
    pa.field("type", pa.string(), True),
    pa.field("name", pa.string(), True),
    pa.field("genre_tag", pa.string(), True),
    pa.field("description", pa.string(), True),
    pa.field("image", pa.string(), True),
    pa.field("platforms_links", pa.string(), True)
])

release_schema = {
    'id': ['@id'],
    'type': ['@type'],
    'name': ['name'],
    'format': ['musicReleaseFormat'],
    'currency': ['offers', 'priceCurrency'],
    'price': ['offers', 'price'],
    'availability': ['offers', 'availability'],
    'description': ['description'],
    'image': ['image'],
    'url': ['url'],
    'buy_url': ['offers', 'url']
}

release_schema_parquet = pa.schema([
    pa.field("id", pa.string(), True),
    pa.field("type", pa.string(), True),
    pa.field("name", pa.string(), True),
    pa.field("format", pa.string(), True),
    pa.field("currency", pa.string(), True),
    pa.field("price", pa.float64(), True),
    pa.field("availability", pa.string(), True),
    pa.field("description", pa.string(), True),
    pa.field("image", pa.string(), True),
    pa.field("url", pa.string(), True),
    pa.field("buy_url", pa.string(), True),
])

record_schema = {
    'id': ['item', '@id'],
    'type': ['item', '@type'],
    'name': ['item', 'name'],
    'duration': ['item', 'duration'],
    'duration_sec': ['item', 'duration_secs'],
    'position': ['position'],
    'url': ['item', 'url']
}

record_schema_parquet = pa.schema([
    pa.field("name", pa.string(), True),
    pa.field("duration", pa.string(), True),
    pa.field("duration_sec", pa.int64(), True),
    pa.field("url", pa.string(), True),
    pa.field("id", pa.float64(), True),
    pa.field("type", pa.float64(), True),
    pa.field("postition", pa.float64(), True)
])

album_schema_parquet = pa.schema([
    pa.field("name", pa.string(), True),
    pa.field("duration", pa.string(), True),
    pa.field("duration_sec", pa.int64(), True),
    pa.field("url", pa.string(), True),
    pa.field("id", pa.float64(), True),
    pa.field("type", pa.float64(), True),
    pa.field("postition", pa.float64(), True)
])