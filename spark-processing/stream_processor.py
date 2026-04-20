import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg, window
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

# 1. Dynamically get the installed PySpark version
spark_version = pyspark.__version__
print(f"🚀 Detected PySpark Version: {spark_version}")

# 2. Initialize Spark Session using the dynamic version and Scala 2.12
spark = SparkSession.builder \
    .appName("LiveMarketRadar") \
    .config("spark.jars.packages", f"org.apache.spark:spark-sql-kafka-0-10_2.12:{spark_version}") \
    .getOrCreate()

# Hide excessive Spark logs
spark.sparkContext.setLogLevel("WARN")

# 2. Define the schema of our incoming JSON data
schema = StructType([
    StructField("timestamp", TimestampType(), True),
    StructField("location", StringType(), True),
    StructField("search_keyword", StringType(), True),
    StructField("demand_intensity", IntegerType(), True)
])

print("🚀 Connecting Spark to Redpanda Stream...")

# 3. Read the stream from Redpanda
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:19092") \
    .option("subscribe", "live-market-signals") \
    .option("startingOffsets", "latest") \
    .load()

# option("startingOffsets", "earliest") - This tells Spark: "Go back to the very beginning of the topic and process everything, even if it's old data."

# 4. Parse the JSON data from the Kafka 'value' column
parsed_df = df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# 5. Perform a real-time aggregation (Average demand per location over 10-second tumbling windows)
aggregated_df = parsed_df \
    .withWatermark("timestamp", "10 seconds") \
    .groupBy(
        window(col("timestamp"), "10 seconds"),
        col("location")
    ) \
    .agg(avg("demand_intensity").alias("avg_demand"))

# 6. Output the results to the Console (for testing)
query = aggregated_df \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()