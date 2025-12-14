from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, DoubleType
from pyspark.sql.functions import from_json, col, window, avg, current_timestamp


spark = SparkSession.builder.appName('CryptoKafkaProcessor').getOrCreate()

spark.sparkContext.setLogLevel("ERROR")


df_kafka = spark.readStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers', 'localhost:9092') \
    .option('subscribe', 'crypto-stream') \
    .option('startingOffsets', 'latest').load()

schema = StructType() \
        .add('time', StringType()) \
        .add('price', DoubleType()) \
        .add('symbol', StringType())

df = df_kafka.selectExpr("CAST(value AS STRING) as STRING") \
    .select(from_json(col('STRING'), schema).alias('data')) \
    .select('data.*')

analyzed_df = df.withColumn('processing_time', current_timestamp()) \
        .groupBy(
            window(col('processing_time'), '10 seconds'), col('symbol')
        ).agg(avg('price')).alias('avg_price')

query = analyzed_df.writeStream \
        .outputMode('complete') \
        .format('console') \
        .option('truncate', 'false') \
        .start()

query.awaitTermination()