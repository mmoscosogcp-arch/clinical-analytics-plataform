from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp


PROJECT_ID = "clinical-analytics-dev"
BUCKET = "clinical-analytics-dev-raw"
INPUT_PATH = f"gs://{BUCKET}/raw/structured_medical_records.csv"
BQ_TABLE = f"{PROJECT_ID}.raw.medical_records"


def main():

    spark = SparkSession.builder \
        .appName("procesos_medical_records") \
        .config("spark.sql.parquet.int96RebaseModeInWrite", "CORRECTED") \
        .config("spark.sql.parquet.datetimeRebaseModeInWrite", "CORRECTED") \
        .getOrCreate()

    df = spark.read.csv(INPUT_PATH, header=True, inferSchema=True)

    df_clean = df.select(
        col("subject_id"),
        col("hadm_id"),
        to_timestamp(col("adm_date")).alias("adm_date"),
        col("adm_time"),
        col("medical_report")
    )

    df_clean.write \
        .format("bigquery") \
        .option("table", BQ_TABLE) \
        .option("temporaryGcsBucket", BUCKET) \
        .option("writeDisposition", "WRITE_TRUNCATE") \
        .mode("overwrite") \
        .save()

    spark.stop()


if __name__ == "__main__":
    main()
