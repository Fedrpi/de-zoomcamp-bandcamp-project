locals {
  data_lake_bucket = "dtc_data_lake"
}

variable "project" {
  description = "Your GCP Project ID"
}

variable "billing_account_id" {
  description = "Your Billing Account ID"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "europe-west6"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "bandcamp"
}

variable "vm_image" {
  description = "Base image for your Virtual Machine."
  type = string
  default = "projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20230125"
}

variable "public_key_path" {
  description = "Path to public ssh key to remote login to vm"
  type = string
  default = "~/.ssh/gcp_datatalk.pub"
}