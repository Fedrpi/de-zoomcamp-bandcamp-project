# Connect to compute engine
To connect to compute engine run this command `ssh -i ~./<path to your privete key> <username>@<compute engine ip>`

# Setup solution with docker compose
Read [docker-compose.yaml](../docker-compose.yaml) and set necessary enviroments variables
We will use docker compose commands in next steps:
- prefect
- dbt docs
- elementary
- metabase

## Prefect
Opensource ETL tool https://www.prefect.io/
For working with prefect docker-compose file have next profiles:
- `server` for prefect database and orion server
- `agent` to run prefect flows in container
- `cli` to work with prefect over command line

To run prefect server use command `docker-compose --profile server up` server will work on port 4200 to access it use http://<your GCP compute engine IP>:4200/ 
To run prefect agent use command `docker-compose --profile agent up`
To run prefect cli use command `docker-compose cli run`

### Deploy flows to GCS
To deploy prefect flows follow next steps:
1. Use command `docker ps` to define container id for prefect cli
2. Use command `docker exec -it <ci container id> bash` to enter to container
3. Move to folder flows by command `cd flows`
4. Install dependencies `pip install -r reuirements.txt`
5. Move to folder deployments `cd deployments`
6. For each python file inside run command `python <file_name.py>`

Now you can access to deployments over Prefect UI and configure shedule or run flows

### Run flows manually
To run flows manually follow next steps:
1. Use command `docker ps` to define container id for prefect cli
2. Use command `docker exec -it <ci container id> bash` to enter to container
3. Move to folder flows by command `cd flows`
4. Install dependencies `pip install -r reuirements.txt`
5. For each python file inside run command `python <file_name.py>`  
Use next order:
    1. bc_upload_raw_to_gcp.py
    2. bc_trasform_and_upload_to_gcs.py
6. Move to folder dbt by command `cd dbt`
7. For each python file inside run command `python <file_name.py>`  
Use next order:
    1. dbt_stg.py
    2. dbt_marts.py
    3. dbt_docs_gen.py
    4. elementary_report.py

Now you can check GCS and Big Query storage and find out bandcamp data

## Dbt Docs
Dbt is opensource data transformation tool https://www.getdbt.com/ It also allows to create great data documentation
To access dbt model documentation run command `docker-compose --profile dbt-docs up` dbt document server will work on port 8080 to access it use http://<your GCP compute engine IP>:8080/

## Elementary
Elementary is opensource tool allows users to monitoring health of dwh that manages by dbt
To run Elementary for DBT use command `docker-compose --profile dbt-elementary up` elementary report will work on port 8081 to access it use http://<your GCP compute engine IP>:8081/

## Metabase
To run Metabase use command `docker-compose --profile metabase up` matabase will work on port 3000 to access it use http://<your GCP compute engine IP>:3000/

