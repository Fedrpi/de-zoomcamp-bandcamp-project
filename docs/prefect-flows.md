# Setup Prefect
To run Prefect use commands:
- `docker-compose --profile server up` to run Prefect server
- `docker-compose --profile agent up` to run Prefect agent
- `docker-compose run cli` to run Prefect cli

# Configure Prefect
Open next url in browser http://<compute-engine-ip>:4200

Go to blocks menu create:
- GCS
- GCS Bucket
- GCS Credentials

# Deploy flows
Go to the container with cli run command `docker exec -it <container id> bash`
In container move to flows folder and install python dependencies:
- `cd flows`
- `pip install -r requirements.txt`

Move to deployments folder and deploy flows:
- `cd deployments`
- `python bc_upload_deployment.py`
- `python bc_trasform_load_deployment.py`