#*********************************SNS Topics**********************************#

#Creating a Topic#

# Initialize boto3 client for SNS
sns = boto3.client('sns',
                   region_name='us-east-1',
                   aws_access_key_id=AWS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET)

# Create the city_alerts topic
response = sns.create_topic(Name="city_alerts")
c_alerts_arn = response['TopicArn']

# Re-create the city_alerts topic using a oneliner
c_alerts_arn_1 = sns.create_topic(Name='city_alerts')['TopicArn']

# Compare the two to make sure they match
print(c_alerts_arn == c_alerts_arn_1)

#*****************************************************************************#

#Creating multiple topics#

# Create list of departments
departments = ['trash', 'streets', 'water']

for dept in departments:
  	# For every department, create a general topic
    sns.create_topic(Name="{}_general".format(dept))

    # For every department, create a critical topic
    sns.create_topic(Name="{}_critical".format(dept))

# Print all the topics in SNS
response = sns.list_topics()
print(response['Topics'])

#*****************************************************************************#

#Deleting multiple topics#

# Get the current list of topics
topics = sns.list_topics()['Topics']

for topic in topics:
  # For each topic, if it is not marked critical, delete it
  if "critical" not in topic['TopicArn']:
    sns.delete_topic(TopicArn=topic['TopicArn'])

# Print the list of remaining critical topics
print(sns.list_topics()['Topics'])

#*****************************************************************************#

#****************************SNS Subscriptions********************************#