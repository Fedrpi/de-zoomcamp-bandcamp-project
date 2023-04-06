import sys
sys.path.append('../dbt')
from dbt_stg import *
from prefect.deployments import Deployment
from prefect.filesystems import GCS
storage = GCS.load("flow-storage")

deployment = Deployment.build_from_flow(
    flow=trigger_dbt_flow,
    name="dbt_stg",
    version='1.0.0',
    storage=storage,
    tags=['raw'],
    parameters={}
)

if __name__ == "__main__":
    deployment.apply()