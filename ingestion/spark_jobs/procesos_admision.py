from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp


PROJECT_ID = "clinical-analytics-dev"
BUCKET = "clinical-analytics-dev-raw"
INPUT_PATH = f"gs://{BUCKET}/raw/ADMISSIONS.csv"
BQ_TABLE = f"{PROJECT_ID}.raw.admisiones"


def main():
    spark = SparkSession.builder \
        .appName("procesos_adimisiones") \
        .config("spark.sql.parquet.int96RebaseModeInWrite", "CORRECTED") \
        .config("spark.sql.parquet.datetimeRebaseModeInWrite", "CORRECTED") \
        .getOrCreate()

    df = spark.read.csv(INPUT_PATH, header=True, inferSchema=True)

    df_clean = df.select(
        col("subject_id"),
        col("hadm_id"),
        col("admission_type"),
        col("ethnicity"),
        col("insurance"),
        col("diagnosis"),
        col("discharge_location"),
        col("hospital_expire_flag").cast("integer"),
        to_timestamp(col("admittime")).alias("admittime"),
        to_timestamp(col("dischtime")).alias("dischtime")
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
