import sys
sys.path.append('../dbt')
from dbt_docs_gen import *
from prefect.deployments import Deployment
from prefect.filesystems import GCS
storage = GCS.load("flow-storage")

deployment = Deployment.build_from_flow(
    flow=trigger_dbt_flow,
    name="dbt_docs_generate",
    version='1.0.0',
    storage=storage,
    tags=['raw', 'dbt'],
    parameters={}
)

if __name__ == "__main__":
    deployment.apply()