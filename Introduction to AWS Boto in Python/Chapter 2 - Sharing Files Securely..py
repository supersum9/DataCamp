#***************************Keeping objects secure****************************#

#Uploading a public report#

# Upload the final_report.csv to gid-staging bucket
s3.upload_file(
  # Complete the filename
  Filename='./final_report.csv',
  # Set the key and bucket
  Key='2019/final_report_2019_02_20.csv',
  Bucket='gid-staging',
  # During upload, set ACL to public-read
  ExtraArgs = {
    'ACL': 'public-read'})

#*****************************************************************************#

#Making multiple files public#

# List only objects that start with '2019/final_'
response = s3.list_objects(
    Bucket='gid-staging', Prefix='2019/final_')

# Iterate over the objects
for obj in response['Contents']:

    # Give each object ACL of public-read
    s3.put_object_acl(Bucket='gid-staging',
                      Key=obj['Key'],
                      ACL='public-read')

    # Print the Public Object URL for each object
    print("https://{}.s3.amazonaws.com/{}".format( 'gid-staging', obj['Key']))

#*****************************************************************************#

#*******************Accessing private objects in S3***************************#

#Generating a presigned URL#

# Generate presigned_url for the uploaded object
share_url = s3.generate_presigned_url(
  # Specify allowable operations
  ClientMethod='get_object',
  # Set the expiration time
  ExpiresIn= 3600,
  # Set bucket and shareable object's name
  Params={'Bucket': 'gid-staging','Key': 'final_report.csv'}
)

# Print out the presigned URL
print(share_url)

#*****************************************************************************#

#Opening a private file#

df_list =  [ ]

for file in response['Contents']:
    # For each file in response load the object from S3
    obj = s3.get_object(Bucket='gid-requests', Key=file['Key'])
    # Load the object's StreamingBody with pandas
    obj_df = pd.read_csv(obj['Body'])
    # Append the resulting DataFrame to list
    df_list.append(obj_df)

# Concat all the DataFrames with pandas
df = pd.concat(df_list)

# Preview the resulting DataFrame
df.head()

#*****************************************************************************#

#***********************Sharing files through a website***********************#

#Generate HTML table from Pandas#

# Generate an HTML table with no border and selected columns
services_df.to_html('./services_no_border.html',
           # Keep specific columns only
           columns=['service_name', 'link'],
           # Set border
           border=0)

# Generate an html table with border and all columns.
services_df.to_html('./services_border_all_columns.html',
           border=1)

#*****************************************************************************#

#Upload an HTML file to S3#

# Upload the lines.html file to S3
s3.upload_file(Filename='lines.html',
               # Set the bucket name
               Bucket='datacamp-public', Key='index.html',
               # Configure uploaded file
               ExtraArgs = {
                 # Set proper content type
                 'ContentType':'text/html',
                 # Set proper ACL
                 'ACL': 'public-read'})

# Print the S3 Public Object URL for the new file.
print("http://{}.s3.amazonaws.com/{}".format('datacamp-public', 'index.html'))

#*****************************************************************************#

#*****************Case Study: Generating a Report Repository******************#

#Combine daily requests for February#

df_list = []

# Load each object from s3
for file in request_files:
    s3_day_reqs = s3.get_object(Bucket='gid-requests',
                                Key=file['Key'])
    # Read the DataFrame into pandas, append it to the list
    day_reqs = pd.read_csv(s3_day_reqs['Body'])
    df_list.append(day_reqs)

# Concatenate all the DataFrames in the list
all_reqs = pd.concat(df_list)

# Preview the DataFrame
all_reqs.head()

#*****************************************************************************#

#Upload aggregated reports for February#

# Write agg_df to a CSV and HTML file with no border
agg_df.to_csv('./feb_final_report.csv')
agg_df.to_html('./feb_final_report.html', border=0)

# Upload the generated CSV to the gid-reports bucket
s3.upload_file(Filename='./feb_final_report.csv',
	Key='2019/feb/final_report.html', Bucket='gid-reports',
    ExtraArgs = {'ACL': 'public-read'})

# Upload the generated HTML to the gid-reports bucket
s3.upload_file(Filename='./feb_final_report.html',
	Key='2019/feb/final_report.html', Bucket='gid-reports',
    ExtraArgs = {'ContentType': 'text/html',
                 'ACL': 'public-read'})

#*****************************************************************************#

#Update index to include February#

# List the gid-reports bucket objects starting with 2019/
objects_list = s3.list_objects(Bucket='gid-reports', Prefix='2019/')

# Convert the response contents to DataFrame
objects_df = pd.DataFrame(objects_list['Contents'])

# Create a column "Link" that contains Public Object URL
base_url = "http://gid-reports.s3.amazonaws.com/"
objects_df['Link'] = base_url + objects_df['Key']

# Preview the resulting DataFrame
objects_df.head()

#*****************************************************************************#

#Upload the new index#

# Write objects_df to an HTML file
objects_df.to_html('report_listing.html',
    # Set clickable links
    render_links=True,
	# Isolate the columns
    columns=['Link', 'LastModified', 'Size'])

# Overwrite index.html key by uploading the new file
s3.upload_file(
  Filename='./report_listing.html', Key='index.html',
  Bucket='gid-reports',
  ExtraArgs = {
    'ContentType': 'text/html',
    'ACL': 'public-read'
  })

#*****************************************************************************#