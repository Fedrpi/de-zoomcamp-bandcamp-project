terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

######################
#                    #
#      Provider      #
#                    #
######################

provider "google" {
  project = var.project
  region = var.region
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

######################
#                    #
#      Resourse      #
#                    #
######################

resource "google_project" "dtc-bandcamp-project" {
  name       = "dtc-bandcamp-project"
  project_id = var.project
  billing_account = var.billing_account_id
}

resource "google_project_service" "compute_engine" {
  project = var.project
  service = "compute.googleapis.com"
}

resource "google_project_service" "iam" {
  project = var.project
  service = "iam.googleapis.com"
}

resource "google_project_service" "bigquery" {
  service = "bigquery.googleapis.com"

  project = var.project
}

resource "google_project_service" "cloud_storage" {
  service = "storage-component.googleapis.com"

  project = var.project
}

######################
#                    #
#       Bucket       #
#                    #
######################

resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${local.data_lake_bucket}_${var.project}"
  location      = var.region
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

resource "google_storage_bucket" "raw-data-lake-bucket" {
  name          = "raw-data-${var.project}"
  location      = var.region
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

resource "google_storage_bucket" "dbt-elementary-bucket" {
  name          = "dbt-elementary-${var.project}" # Concatenating DL bucket & Project name for unique naming
  location      = var.region
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

resource "google_storage_bucket" "prefect-flow-bucket" {
  name          = "prefect-flow-${var.project}" # Concatenating DL bucket & Project name for unique naming
  location      = var.region
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

######################
#                    #
#       Dataset      #
#                    #
######################

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.region
}

resource "google_bigquery_dataset" "dbt_bandcamp" {
  dataset_id = "dbt_bandcamp"
  project    = var.project
  location   = var.region
}

resource "google_bigquery_dataset" "dbt_elementary" {
  dataset_id = "dbt_elementary"
  project    = var.project
  location   = var.region
}

######################
#                    #
#   Compute Engine   #
#                    #
######################

resource "google_compute_instance" "vm_instance" {
  name          = "bandcamp-instance"
  project       = var.project
  machine_type  = "e2-standard-4"
  zone          = "${var.region}-a"
  depends_on = [
    google_project_service.compute_engine,
  ]

  boot_disk {
    initialize_params {
      image = var.vm_image
      size  = "30"
      type  = "pd-balanced"
    }
  }
  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }
  metadata = {
    ssh-keys = "fedrpi:${file(var.public_key_path)}"
  }
  metadata_startup_script = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y docker.io python3 git curl
    curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    EOF
}

######################
#                    #
#      Firewall      #
#                    #
######################

resource "google_compute_firewall" "dbt" {
  name    = "dbt"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["80", "8080", "8081"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "metabase" {
  name    = "metabase"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["3000"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "prefect" {
  name    = "prefect"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["4200"]
  }

  source_ranges = ["0.0.0.0/0"]
}

######################
#                    #
#  Service Account   #
#                    #
######################

resource "google_service_account" "owner_service_account" {
  account_id   = "owner-${var.project}"
  display_name = "owner service account"
  project       = var.project
}

resource "google_service_account" "prefect_service_account" {
  account_id   = "prefect-${var.project}"
  display_name = "prefect service account"
  project       = var.project
}

resource "google_service_account" "dbt_service_account" {
  account_id   = "dbt-${var.project}"
  display_name = "dbt service account"
  project       = var.project
}

######################
#                    #
#      IAM Roles     #
#                    #
######################

resource "google_project_iam_member" "owner" {
  for_each = toset([
    "roles/bigquery.admin",
    "roles/bigquery.dataOwner",
    "roles/storage.admin",
    "roles/storage.objectAdmin"
  ])
  role = each.key
  member = "serviceAccount:${google_service_account.owner_service_account.email}"
  project = var.project
  depends_on = [
    google_project_service.iam,
  ]
}

resource "google_project_iam_member" "prefect" {
  for_each = toset([
    "roles/bigquery.admin",
    "roles/bigquery.dataOwner",
    "roles/storage.admin",
    "roles/storage.objectAdmin"
  ])
  role = each.key
  member = "serviceAccount:${google_service_account.prefect_service_account.email}"
  project = var.project
  depends_on = [
    google_project_service.iam,
  ]
}

resource "google_project_iam_member" "dbt" {
  for_each = toset([
    "roles/bigquery.admin",
    "roles/bigquery.dataOwner",
    "roles/storage.admin",
    "roles/storage.objectAdmin"
  ])
  role = each.key
  member = "serviceAccount:${google_service_account.dbt_service_account.email}"
  project = var.project
  depends_on = [
    google_project_service.iam,
  ]
}