#Examining The SparkContext#

# Verify SparkContext
print(sc)

# Print Spark version
print(sc.version)

#*****************************************************************************#

#Creating a SparkSession#

# Import SparkSession from pyspark.sql
from pyspark.sql import SparkSession

# Create my_spark
my_spark = SparkSession.builder.getOrCreate()

# Print my_spark
print(my_spark)

#*****************************************************************************#

#Viewing tables#

# Print the tables in the catalog
print(spark.catalog.listTables())

#*****************************************************************************#

#Are you query-ious?#

# Don't change this query
query = "FROM flights SELECT * LIMIT 10"

# Get the first 10 rows of flights
flights10 = spark.sql(query)

# Show the results
flights10.show()

#*****************************************************************************#

#Pandafy a Spark DataFrame#
# Don't change this query
query = "SELECT origin, dest, COUNT(*) as N FROM flights GROUP BY origin, dest"

# Run the query
flight_counts = spark.sql(query)

# Convert the results to a pandas DataFrame
pd_counts = flight_counts.toPandas()

# Print the head of pd_counts
print(pd_counts.head())

#*****************************************************************************#

#Put some Spark in your data#

# Create pd_temp
pd_temp = pd.DataFrame(np.random.random(10))

# Create spark_temp from pd_temp
spark_temp = spark.createDataFrame(pd_temp)

# Examine the tables in the catalog
print(spark.catalog.listTables())

# Add spark_temp to the catalog
spark_temp.createOrReplaceTempView('temp')

# Examine the tables in the catalog again
print(spark.catalog.listTables())

#*****************************************************************************#

#Dropping the middle man#

# Don't change this file path
file_path = "/usr/local/share/datasets/airports.csv"

# Read in the airports data
airports = spark.read.csv(file_path, header=True)

# Show the data
print(airports.show())

#*****************************************************************************#