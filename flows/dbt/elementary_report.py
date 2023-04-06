from prefect import flow
from prefect_shell import ShellOperation

@flow
def run_elementary_report():
    ShellOperation(
        commands=[
            "edr report --profiles-dir ${profiles_dir} --project-dir ${project_dir} --file-path ${file_path}"
        ],
        env={"project_dir": "/root/dbt_bc",
             "profiles_dir": "/root/keys",
             "file_path": "/root/dbt_bc/elementary_report/index.html"}
    ).run()
    
    return None

run_elementary_report()
