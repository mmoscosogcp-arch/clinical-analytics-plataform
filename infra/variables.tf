variable "project_id" {
    description = "Id del proyecto en GCP"
    type        = string
    default     = "clinical-analytics-dev"
}

variable "region" {
    description = "Region donde se crean los recursos"
    type        = string
    default     = "us-central1"
}

variable "credentials_file" {
    description = "Ruta al archivo de credenciales de la service account"
    type        = string
    default     = "clinical-analytics-dev-e1fef7af3102.json"
}