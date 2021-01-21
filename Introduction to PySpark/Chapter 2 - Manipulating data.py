#Creating columns#

# Create the DataFrame flights
flights = spark.table('flights')

# Show the head
print(flights.show())

# Add duration_hrs
flights = flights.withColumn('duration_hrs', flights.air_time/60)

#*****************************************************************************#

#Filtering Data#

# Filter flights by passing a string
long_flights1 = flights.filter('distance > 1000')

# Filter flights by passing a column of boolean values
long_flights2 = flights.filter(flights.distance > 1000)

# Print the data to check they're equal
print(long_flights1.show())
print(long_flights2.show())

#*****************************************************************************#

#Selecting#

# Select the first set of columns
selected1 = flights.select('tailnum','origin','dest')

# Select the second set of columns
temp = flights.select(flights.origin, flights.dest, flights.carrier)

# Define first filter
filterA = flights.origin == "SEA"

# Define second filter
filterB = flights.dest == "PDX"

# Filter the data, first by filterA then by filterB
selected2 = temp.filter(filterA).filter(filterB)

#*****************************************************************************#

#Selecting II#

# Define avg_speed
avg_speed = (flights.distance/(flights.air_time/60)).alias("avg_speed")

# Select the correct columns
speed1 = flights.select("origin", "dest", "tailnum", avg_speed)

# Create the same table using a SQL expression
speed2 = flights.selectExpr("origin", "dest", "tailnum", \
    "distance/(air_time/60) as avg_speed")

#*****************************************************************************#

#Aggregating#

# Find the shortest flight from PDX in terms of distance
flights.filter(flights.origin == 'PDX').groupBy().min('distance').show()

# Find the longest flight from SEA in terms of air time
flights.filter(flights.origin == 'SEA').groupBy().max('air_time').show()

#*****************************************************************************#

#Aggregating II#

# Average duration of Delta flights
flights.filter(flights.carrier=='DL').filter(flights.origin=='SEA').\
    groupBy().avg('air_time').show()

# Total hours in the air
flights.withColumn("duration_hrs", flights.air_time/60).groupBy().\
    sum('duration_hrs').show()

#*****************************************************************************#

#Grouping and Aggregating I#

# Group by tailnum
by_plane = flights.groupBy("tailnum")

# Number of flights each plane made
by_plane.count().show()

# Group by origin
by_origin = flights.groupBy("origin")

# Average duration of flights from PDX and SEA
by_origin.avg("air_time").show()

#*****************************************************************************#

#Grouping and Aggregating II#

# Import pyspark.sql.functions as F
import pyspark.sql.functions as F

# Group by month and dest
by_month_dest = flights.groupBy('month','dest')

# Average departure delay by month and destination
by_month_dest.avg('dep_delay').show()

# Standard deviation of departure delay
by_month_dest.agg(F.stddev('dep_delay')).show()

#*****************************************************************************#

#Joining II#

# Examine the data
print(airports.show())

# Rename the faa column
airports = airports.withColumnRenamed('faa','dest')

# Join the DataFrames
flights_with_airports = flights.join(airports,on='dest',how='leftouter')

# Examine the new DataFrame
print(flights_with_airports.show())

#*****************************************************************************#