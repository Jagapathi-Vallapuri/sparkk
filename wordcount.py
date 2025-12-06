from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, col, lower, desc

sparkSession = SparkSession.builder.appName('WordCount').master("local[*]").getOrCreate()


text_df = sparkSession.read.text('romeo')

words_df = text_df.select(
    explode(split(col("value"), " ")).alias('word')
)

cleaned_words_df = words_df.select(
    lower(col('word')).alias('word')).filter(col('word') != "")


count_df = cleaned_words_df.groupBy('word').count()

ordered_words = count_df.orderBy(desc('count'))
print('Top 20 words: ')
ordered_words.show(20)

sparkSession.stop()