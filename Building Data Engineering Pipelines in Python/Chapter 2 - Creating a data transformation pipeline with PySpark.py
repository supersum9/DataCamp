#*********************Basic introduction to PySpark***************************#

#Reading a CSV file#

# Read a csv file and set the headers
df = (spark.read
      .options(header=True)
      .csv("/home/repl/workspace/mnt/data_lake/landing/ratings.csv"))

df.show()

#*****************************************************************************#

#Defining a schema#

# Define the schema
schema = StructType([
  StructField("brand", StringType(), nullable=False),
  StructField("model", StringType(), nullable=False),
  StructField("absorption_rate", ByteType(), nullable=True),
  StructField("comfort", ByteType(), nullable=True)
])

better_df = (spark
             .read
             .options(header="true")
             # Pass the predefined schema to the Reader
             .schema(schema)
             .csv("/home/repl/workspace/mnt/data_lake/landing/ratings.csv"))
pprint(better_df.dtypes)

#*****************************************************************************#

#***************************Cleaning data*************************************#

#Removing invalid rows#

# Specify the option to drop invalid rows
ratings = (spark
           .read
           .options(header=True, mode='DROPMALFORMED')
           .csv("/home/repl/workspace/mnt/data_lake/landing/ratings_with_invalid_rows.csv"))
ratings.show()

#*****************************************************************************#

print("BEFORE")
ratings.show()

print("AFTER")
# Replace nulls with arbitrary value on column subset
ratings = ratings.fillna(4, subset=["comfort"])
ratings.show()

#*****************************************************************************#

#Conditionally replacing values#

from pyspark.sql.functions import col, when

# Add/relabel the column
categorized_ratings = ratings.withColumn(
    "comfort",
    # Express the condition in terms of column operations
    when(col("comfort") > 3, "sufficient").otherwise("insufficient"))

categorized_ratings.show()

#*****************************************************************************#

#*********************Transforming data with Spark****************************#

#Selecting and renaming columns#

from pyspark.sql.functions import col

# Select the columns and rename the "absorption_rate" column
result = ratings.select([col("brand"),
                       col("model"),
                       col("absorption_rate").alias('absorbency')])

# Show only unique values
result.distinct().show()

#*****************************************************************************#

#Grouping and aggregating data#

from pyspark.sql.functions import col, avg, stddev_samp, max as sfmax

aggregated = (purchased
              # Group rows by 'Country'
              .groupBy(col('Country'))
              .agg(
                # Calculate the average salary per group and rename
                avg('Salary').alias('average_salary'),
                # Calculate the standard deviation per group
                stddev_samp('Salary'),
                # Retain the highest salary per group and rename
                sfmax('Salary').alias('highest_salary')
              )
             )

aggregated.show()

#*****************************************************************************#

#*****************************Packaging your application**********************#

#Creating a deployable artifact#

zip --recurse-paths pydaiper.zip pydiaper

#Submitting your Spark job#

spark-submit \
    --py-files spark_pipelines/pydiaper/pydiaper.zip \
      spark_pipelines/pydiaper/pydiaper/cleaning/clean_ratings.py

#*****************************************************************************#