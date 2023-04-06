from prefect import flow
from prefect_dbt.cli.commands import DbtCoreOperation

@flow
def trigger_dbt_flow() -> str:
    result = DbtCoreOperation(
        commands=["dbt docs generate"],
        project_dir="/root/dbt_bc",
        profiles_dir="/root/keys/"
    ).run()
    return result

trigger_dbt_flow()