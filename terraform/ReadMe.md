# Create infrastructure
To manage infrastructure in this project uses tool [Terraform](https://www.terraform.io/)
To install terraform read [documentation](https://developer.hashicorp.com/terraform/downloads)
## Config terraform
1. Enter terraform folder
2. Open file [version.tf](/bandcamp_project/terraform/version.tf)
3. Change variables if nessesary
## Check execute plan
1. Open terminal
2. Enter to terraform folder. If you in project root folder run coomand ```cd terraform```
3. Run command ```terraform plan``` 
   1. Fill your billing id
   2. Fill your project name
   3. Type "yes"
   4. Press enter
4. Check if everything is correct, fix errors if occurs and check everything again
## Apply infrastructure
1. Run command ```terraform apply```
   1. Fill your billing id
   2. Fill your project name
   3. Type "yes"
   4. Press enter
2. Check if everything is correct
3. Go to GCP console 
