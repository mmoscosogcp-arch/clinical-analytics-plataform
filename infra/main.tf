terraform {
    required_providers{
        google = {
            source = "hashicorp/google"
            version = "~> 5.0"
        }
    }
}

provider "google" {
    credentials = file("clinical-analytics-dev-e1fef7af3102.json")
    project = "clinical-analytics-dev"
    region = "us-central1"
}

