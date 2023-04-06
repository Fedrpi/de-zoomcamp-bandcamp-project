import sys
sys.path.append('../dbt')
from elementary_report import run_elementary_report
from prefect.deployments import Deployment
from prefect.filesystems import GCS
storage = GCS.load("flow-storage")

deployment = Deployment.build_from_flow(
    flow=run_elementary_report,
    name="elementary_report",
    version='1.0.0',
    storage=storage,
    tags=['raw'],
    parameters={}
)

if __name__ == "__main__":
    deployment.apply()