from pyspark.sql import SparkSession
from pyspark.sql.functions import col


PROJECT_ID = "clinical-analytics-dev"
BUCKET = "clinical-analytics-dev-raw"
INPUT_PATH = f"gs://{BUCKET}/raw/D_LABITEMS.csv"
BQ_TABLE = f"{PROJECT_ID}.raw.dlabitems"


def main():

    spark = SparkSession.builder \
        .appName("procesos_dlabitems") \
        .config("spark.sql.parquet.int96RebaseModeInWrite", "CORRECTED") \
        .config("spark.sql.parquet.datetimeRebaseModeInWrite", "CORRECTED") \
        .getOrCreate()

    df = spark.read.csv(INPUT_PATH, header=True, inferSchema=True)

    df_clean = df.select(
        col("itemid"),
        col("label"),
        col("fluid"),
        col("category"),
        col("loinc_code")
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
