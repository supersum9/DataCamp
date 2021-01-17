#Creating columns#

# Create the DataFrame flights
flights = spark.table('flights')

# Show the head
print(flights.show())

# Add duration_hrs
flights = flights.withColumn('duration_hrs', flights.air_time/60)

#*****************************************************************************#

