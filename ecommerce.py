from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, round, desc

spark = SparkSession.builder.appName('Ecommerce').master("local[*]").getOrCreate()


df = spark.read.csv("sales.csv", header=True, inferSchema=True)

df.printSchema()

df_with_revenue = df.withColumn('Revenue', col('Price') * col('Quantity'))

country_revenue = df_with_revenue.groupBy('Country').agg(sum('Revenue').alias('TotalRevenue')).orderBy(desc('TotalRevenue'))

country_revenue.show()

df.createOrReplaceTempView('sales')

sql_query = """
    SELECT Product, SUM(Quantity) as TotalQuantity
    FROM sales
    WHERE Country = 'USA'
    GROUP BY Product
    ORDER BY TotalQuantity DESC
"""

product_sales = spark.sql(sql_query)
product_sales.show()

print("\n--- Average Spend per Customer ---")
customer_spend = spark.sql("""
    SELECT CustomerID, ROUND(SUM(Price * Quantity), 2) as TotalSpend
    FROM sales
    GROUP BY CustomerID
    ORDER BY TotalSpend DESC
    LIMIT 5
""")

customer_spend.show()

spark.stop()