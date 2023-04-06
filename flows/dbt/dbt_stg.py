from prefect import flow
from prefect_dbt.cli.commands import DbtCoreOperation

@flow
def trigger_dbt_flow() -> str:
    result = DbtCoreOperation(
        commands=["dbt test --vars '{is_test_run: false}'", 
                  "dbt run --exclude fact_music_genres --vars '{is_test_run: false}'"],
        project_dir="/root/dbt_bc",
        profiles_dir="/root/keys/"
    ).run()
    return result

trigger_dbt_flow()