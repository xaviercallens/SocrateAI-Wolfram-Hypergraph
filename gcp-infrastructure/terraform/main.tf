# GCP Terraform Configuration for Stream 4 Wolfram CAG Microservices

terraform {
  required_version = ">= 1.3.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.80.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

variable "gcp_project_id" {
  type    = string
  default = "socrate-ai-gcp"
}

variable "gcp_region" {
  type    = string
  default = "us-central1"
}

resource "google_cloud_run_v2_service" "wolfram_mcp_service" {
  name     = "wolfram-mcp-cag-engine"
  location = var.gcp_region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "gcr.io/${var.gcp_project_id}/wolfram-mcp-cag-engine:latest"
      resources {
        limits = {
          cpu    = "2000m"
          memory = "4Gi"
        }
      }
      env {
        name  = "CAG_STRICT_MODE"
        value = "TRUE"
      }
    }
  }
}

output "cloud_run_mcp_url" {
  value = google_cloud_run_v2_service.wolfram_mcp_service.uri
}
