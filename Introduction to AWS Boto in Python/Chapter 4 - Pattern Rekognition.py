#*********************************Rekognizing patterns************************#

#Cat detector#

# Use Rekognition client to detect labels
image1_response = rekog.detect_labels(
    # Specify the image as an S3Object; Return one label
    Image=image1, MaxLabels=1)

# Print the labels
print(image1_response['Labels'])

# Use Rekognition client to detect labels
image2_response = rekog.detect_labels(
    Image= image2, MaxLabels= 1
)

# Print the labels
print(image2_response['Labels'])

#*****************************************************************************#

#Multiple cat detector#

# Create an empty counter variable
cats_count = 0
# Iterate over the labels in the response
for label in response['Labels']:
    # Find the cat label, look over the detected instances
    if label['Name'] == 'Cat':
        for instance in label['Instances']:
            # Only count instances with confidence > 85
            if (instance['Confidence'] > 85):
                cats_count += 1
# Print count of cats
print(cats_count)

#*****************************************************************************#

#Parking sign reader#

# Create empty list of words
words = []
# Iterate over the TextDetections in the response dictionary
for text_detection in response['TextDetections']:
  	# If TextDetection type is WORD, append it to words list
    if text_detection['Type'] == 'WORD':
        # Append the detected text
        words.append(text_detection['DetectedText'])
# Print out the words list
print(words)

###############################

# Create empty list of lines
lines = []
# Iterate over the TextDetections in the response dictionary
for text_detection in response['TextDetections']:
  	# If TextDetection type is Line, append it to lines list
    if text_detection['Type'] == 'LINE':
        # Append the detected text
        lines.append(text_detection['DetectedText'])
# Print out the words list
print(lines)

#*****************************************************************************#

#*************************Comprehending text**********************************#

#Detecting language#

# For each dataframe row
for index, row in dumping_df.iterrows():
    # Get the public description field
    description =dumping_df.loc[index, 'public_description']
    if description != '':
        # Detect language in the field content
        resp = comprehend.detect_dominant_language(Text=description)
        # Assign the top choice language to the lang column.
        dumping_df.loc[index, 'lang'] = resp['Languages'][0]['LanguageCode']

# Count the total number of spanish posts
spanish_post_ct = len(dumping_df[dumping_df.lang == 'es'])
# Print the result
print("{} posts in Spanish".format(spanish_post_ct))

#*****************************************************************************#

#Translating Get It Done requests#

for index, row in dumping_df.iterrows():
  	# Get the public_description into a variable
    description = dumping_df.loc[index, 'public_description']
    if description != '':
      	# Translate the public description
        resp = translate.translate_text(
            Text=description,
            SourceLanguageCode='auto', TargetLanguageCode='en')
        # Store original language in original_lang column
        dumping_df.loc[index, 'original_lang'] = resp['SourceLanguageCode']
        # Store the translation in the translated_desc column
        dumping_df.loc[index, 'translated_desc'] = resp['TranslatedText']
# Preview the resulting DataFrame
dumping_df = dumping_df[['service_request_id', 'original_lang', \
    'translated_desc']]
dumping_df.head()

#*****************************************************************************#

#Getting request sentiment#

for index, row in dumping_df.iterrows():
  	# Get the translated_desc into a variable
    description = dumping_df.loc[index, 'public_description']
    if description != '':
      	# Get the detect_sentiment response
        response = comprehend.detect_sentiment(
          Text=description,
          LanguageCode='en')
        # Get the sentiment key value into sentiment column
        dumping_df.loc[index, 'sentiment'] = response['Sentiment']
# Preview the dataframe
dumping_df.head()

#*****************************************************************************#

#**********************Case Study: Scooting Around!***************************#

#Scooter community sentiment#

for index, row in scooter_requests.iterrows():
  	# For every DataFrame row
    desc = scooter_requests.loc[index, 'public_description']
    if desc != '':
      	# Detect the dominant language
        resp = comprehend.detect_dominant_language(Text=desc)
        lang_code = resp['Languages'][0]['LanguageCode']
        scooter_requests.loc[index, 'lang'] = lang_code
        # Use the detected language to determine sentiment
        scooter_requests.loc[index, 'sentiment'] = comprehend.detect_sentiment(
          Text=desc,
          LanguageCode=lang_code)['Sentiment']
# Perform a count of sentiment by group.
counts = scooter_requests.groupby(['sentiment', 'lang']).count()
counts.head()

#*****************************************************************************#

#Scooter dispatch#

# Get topic ARN for scooter notifications
topic_arn = sns.create_topic(Name='scooter_notifications')['TopicArn']

for index, row in scooter_requests.iterrows():
    # Check if notification should be sent
    if (row['sentiment'] == 'NEGATIVE') & (row['img_scooter'] == 1):
        # Construct a message to publish to the scooter team.
        message = "Please remove scooter at {}, {}. Description: {}".format(
            row['long'], row['lat'], row['public_description'])

        # Publish the message to the topic!
        sns.publish(TopicArn = topic_arn,
                    Message = message,
                    Subject = "Scooter Alert")

#*****************************************************************************#