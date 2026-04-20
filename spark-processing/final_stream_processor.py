import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, FloatType

spark_version = pyspark.__version__
print(f"🚀 Detected PySpark Version: {spark_version}")

spark = SparkSession.builder \
    .appName("LiveMarketRadar") \
    .config("spark.jars.packages", f"org.apache.spark:spark-sql-kafka-0-10_2.12:{spark_version}") \
    .config("spark.jars", "/home/lakshyakukreja7official/gcs-jars/gcs-connector-hadoop3-2.2.22-shaded.jar") \
    .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
    .config("spark.hadoop.fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS") \
    .config("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", "/home/lakshyakukreja7official/gcp_keys.json") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Updated schema to match the producer
schema = StructType([
    StructField("timestamp", TimestampType(), True),
    StructField("city", StringType(), True),
    StructField("search_term", StringType(), True),
    StructField("search_volume", IntegerType(), True),
    StructField("sentiment_score", FloatType(), True)
])

print("🚀 Connecting Spark to Redpanda Stream...")

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:19092") \
    .option("subscribe", "live-market-signals") \
    .option("startingOffsets", "latest") \
    .load()

parsed_df = df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

print("💾 Streaming raw Parquet files to Google Cloud Storage...")


"""
from pyspark.sql.functions import window, avg

# Create a 5-minute tumbling window based on the event timestamp
windowed_df = parsed_df \
    .groupBy(
        window(col("timestamp"), "5 minutes"), 
        col("city")
    ) \
    .agg(
        avg("sentiment_score").alias("avg_sentiment"),
        avg("search_volume").alias("avg_volume")
    )
"""
# above piece of commented code can be used for window or aggregation


# Writing directly to your GCS Data Lake
query = parsed_df \
    .writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "gs://de-zoomcamp-final-project-bucket-7/raw/demand/") \
    .option("checkpointLocation", "gs://de-zoomcamp-final-project-bucket-7/checkpoints/demand/") \
    .trigger(processingTime='2 minute') \
    .start()



query.awaitTermination()