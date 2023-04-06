# import sys
# sys.path.append('../')
from bc_trasform_and_upload_to_gcs import *
import config
from prefect.deployments import Deployment
from prefect.filesystems import GCS
storage = GCS.load("flow-storage")

deployment = Deployment.build_from_flow(
    flow=flow_orchestrator,
    name="upload_bandcamp_to_bigquery",
    version='1.0.0',
    storage=storage,
    tags=['raw'],
    parameters={
        'from_path': 'https://www.dropbox.com/s/a1kl5e35j4o53mz/bandcamp-items-json.zip?dl=1',
        'to_path': 'data/bandcamp.zip',
        'bucket': 'raw-data-dtc-bandcamp-ff',
        'bucket_path': '/data/'
    }
)

if __name__ == "__main__":
    deployment.apply()