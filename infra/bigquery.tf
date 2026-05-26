resource "google_bigquery_dataset" "raw" {
    dataset_id = "raw"
    location = var.region
    description = "Datos limpios sin transformar - salida de Pyspark"
}

resource "google_bigquery_dataset" "curated" {
    dataset_id = "curated"
    location = var.region
    description = "Modelos de negocio - salida de dbt"
}