from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp

PROJECT_ID = "clinical-analytics-dev"
BUCKET = "clinical-analytics-dev-raw"
INPUT_PATH = f"gs://{BUCKET}/raw/LABEVENTS.csv"
BQ_TABLE = f"{PROJECT_ID}.raw.labevents"


def main():
    spark = SparkSession.builder \
        .appName("procesos_labevents") \
        .config("spark.sql.parquet.int96RebaseModeInWrite", "CORRECTED") \
        .config("spark.sql.parquet.datetimeRebaseModeInWrite", "CORRECTED") \
        .getOrCreate()

    df = spark.read.csv(INPUT_PATH, header=True, inferSchema=True)

    df_clean = df.select(
        col("subject_id"),
        col("hadm_id"),
        col("itemid"),
        col("value"),
        col("valuenum"),
        col("valueuom"),
        col("flag"),
        to_timestamp(col("charttime")).alias("charttime")
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
