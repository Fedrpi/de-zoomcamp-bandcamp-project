import pandas as pd
import json
import os
import multiprocessing
from common_func import *
from config import *
from pathlib import Path
from prefect import flow, task
from prefect.filesystems import GCS
from prefect_gcp.cloud_storage import GcsBucket
from prefect_shell import ShellOperation
from prefect_gcp import GcpCredentials


@task(log_prints=True)
def download_data_from_gcs(local_path:str, bucket:str, file_name:str) -> None:
    print(f'load data from gcs gs://{bucket}/{file_name}')
    ShellOperation(
        commands=[
            "gcloud auth activate-service-account --key-file /Users/fdr/SqlProjects/Datatalks/keys/dbt-disco-bedrock-375516-391dce4a8b2b.json",
            "mkdir -p ${local_path}",
            "gcloud storage cp gs://${bucket}/${file_name} ${local_path}"
        ],
        env={"local_path": local_path, "bucket": bucket, "file_name": file_name}
    ).run()

@task(log_prints=True)
def unzip_archive(local_path:str, file_name:str) -> None:
    print(f'Unzip {local_path}{file_name} and remove archive')
    ShellOperation(
        commands=[
            "unzip -d ${local_path} ${local_path}${file_name}",
            "rm ${local_path}${file_name}"
        ],
        env={"local_path": local_path, "file_name": file_name}
    ).run()

@task(log_prints=True)
def get_main_df(path):
    print(f'load file {path}')
    with open(path) as f:
        json_data = f.read()
    data = json.loads(json_data)
    df = pd.read_json(data, orient='records')
    # keep only albums
    df = df[df['@type'] == 'MusicAlbum']
    return df

@task(log_prints=True)
def calc_artist_df(main_df):
    print('trasform artists')
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")
    artist_df = pd.DataFrame()
    artist_df['data'] = main_df.apply(get_data, 
                                      field='byArtist', 
                                      schema=artist_schema, 
                                      axis=1)

    artist_df = artist_df['data'].apply(pd.Series)
    artist_df = artist_df.astype({'platforms_links':'str'})#.drop_duplicates()

    # modify main_df
    main_df['artist_id'] = artist_df['id']

    # artist_df.to_parquet(f'{result_path}', schema=artist_schema_parquet)
    print('load artists')
    artist_df.to_gbq(
        destination_table="bandcamp.artist",
        project_id="disco-bedrock-375516",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        location="europe-west6",
        if_exists="append",
    )

@task(log_prints=True)
def calc_release_df(main_df):
    print('trasform release')
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")
    release_df = pd.DataFrame()
    release_df['data'] = main_df.apply(get_data_list, 
                                       field='albumRelease', 
                                       schema=release_schema, 
                                       axis=1)
    release_df = release_df[release_df['data'].apply(lambda x: len(x)) > 0]
    
    release_df = release_df['data'].explode().apply(pd.Series)
    release_df = release_df.astype({'image':'str', 'type':'str'})
    release_df['album_id'] = main_df['_id']
    
    # release_df.to_parquet(f'{result_path}', schema=release_schema_parquet)

    print('load release')
    release_df.to_gbq(
        destination_table="bandcamp.release",
        project_id="disco-bedrock-375516",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        location="europe-west6",
        if_exists="append",
    )

@task(log_prints=True)
def calc_record_df(main_df):
    print('transform record')
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")
    record_df = pd.DataFrame()
    record_df['data'] = main_df['track'].apply(get_data_list, 
                                               field='itemListElement', 
                                               schema=record_schema)
    record_df = record_df[record_df['data'].apply(lambda x: len(x)) > 0]

    record_df = record_df['data'].explode().apply(pd.Series)
    record_df = record_df.astype({'type':'str'})
    record_df['album_id'] = main_df['_id']

    # record_df.to_parquet(f'{result_path}')
    print('load record')
    record_df.to_gbq(
        destination_table="bandcamp.record",
        project_id="disco-bedrock-375516",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        location="europe-west6",
        if_exists="append",
    )

@task(log_prints=True)
def calc_album_df(main_df):
    print('transform album')
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")
    album_df = main_df.copy()
    album_df.drop(columns=['byArtist', 
                           'albumRelease', 
                           'track', 
                           'duration_secs',
                           '@context',
                           '@type',
                           '@id',
                        #    '@graph',
                           'duration',
                           'offers',
                           'url',
                           'isrcCode',
                           'recordingOf',
                           'inAlbum',
                           'comment'], inplace=True)
    try:
        album_df.drop(columns=['@graph'], inplace=True)
    except Exception as e:
        pass
    album_df.rename(columns={'_id':'id'}, inplace=True)

    # album_df.to_parquet(f'{result_path}')
    print('load album')
    album_df.to_gbq(
        destination_table="bandcamp.album",
        project_id="disco-bedrock-375516",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        location="europe-west6",
        if_exists="append"
    )


@flow()
def flow_orchestrator(local_path:str, bucket:str, file_name:str) -> None:
    """Task orchestrator
    :param str dataset_url: path to file in web
    :param str dataset_file: name of file with data
    :param str data_path: path to save file
    """
    # download_data_from_gcs(local_path, bucket, file_name)
    # unzip_archive(local_path, file_name)
    for dirpath, dirnames, filenames in os.walk(local_path):
        for filename in filenames:
            if filename.endswith('.json'):
                file_path = os.path.join(dirpath, filename)
                df = get_main_df(file_path)
                calc_artist_df(df)
                # calc_release_df(df)
                # calc_record_df(df)
                calc_album_df(df)

if __name__ == "__main__":
    local_path = './data/bc/'
    file_name = 'bandcamp.zip'
    bucket = 'bandcamp-disco-bedrock-375516'
    flow_orchestrator(local_path, bucket, file_name)
