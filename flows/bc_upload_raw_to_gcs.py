import pandas as pd
import re
from pathlib import Path
import urllib.request
from prefect import flow, task
from prefect.filesystems import GCS
from prefect_gcp.cloud_storage import GcsBucket
from prefect_shell import ShellOperation

@task(log_prints=True)
def download_data(from_path:str, to_path:str):
    print(f'Download data from {from_path} to {to_path}')
    ShellOperation(
        commands=[
            "wget -nv -c -x -O ${to_path} ${from_path}",
        ],
        env={"from_path": from_path, "to_path": to_path}
    ).run()

# @task(log_prints=True)
# def upload_data_gcs(local_path:str, bucket:str, bucket_path:str) -> None:
#     print(f'Upload data from {local_path} to gs://{bucket}{bucket_path}')
#     ShellOperation(
#         commands=[
#             "gcloud auth activate-service-account --key-file ./keys/dbt-disco-bedrock-375516-391dce4a8b2b.json",
#             "gcloud storage cp ${local_path} gs://${bucket}${bucket_path}"
#         ],
#         env={"local_path": local_path, "bucket": bucket, "bucket_path": bucket_path}
#     ).run()

@task(log_prints=True)
def upload_data_gcs(local_path:str, bucket:str, bucket_path:str) -> None:
    """Upload local parquet file to GCS
    :param Path path: path to file for upload
    """
    print(f'Upload data from {local_path} to gs://{bucket}{bucket_path}')
    gcs_block = GcsBucket.load("bandcamp-lake")
    gcs_block.upload_from_path(from_path=local_path, to_path=f'{bucket_path}')
    return


@task(log_prints=True)
def clear_local_path(local_path:str) -> None:
    ShellOperation(
        commands=[
            "rm ${local_path}"
        ],
        env={"local_path": local_path}
    ).run()

@flow()
def upload_to_gcs(from_path:str, to_path:str, bucket:str, bucket_path:str) -> None:
    """Task orchestrator
    :param str dataset_url: path to file in web
    :param str dataset_file: name of file with data
    :param str data_path: path to save file
    """
    download_data(from_path, to_path)
    # upload_data_gcs(to_path, bucket, bucket_path)
    # clear_local_path(to_path)


if __name__ == "__main__":
    from_path = 'https://www.dropbox.com/s/a1kl5e35j4o53mz/bandcamp-items-json.zip?dl=1'
    to_path = './data/bandcamp.zip'
    bucket = 'raw-data-dtc-bandcamp-ff'
    bucket_path = 'data/bandcamp.zip'
    upload_to_gcs(from_path, to_path, bucket, bucket_path)
