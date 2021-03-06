#*************************What is data preprocessing?*************************#
#Missing data - rows#

# Check how many values are missing in the category_desc column
print(volunteer['category_desc'].isnull().sum())

# Subset the volunteer dataset
volunteer_subset = volunteer[volunteer['category_desc'].notnull()]

# Print out the shape of the subset
print(volunteer_subset.shape)

#*****************************************************************************#

#************************Working with data types******************************#

#Converting a column type#

# Print the head of the hits column
print(volunteer["hits"].head())

# Convert the hits column to type int
volunteer["hits"] = volunteer['hits'].astype(int)

# Look at the dtypes of the dataset
print(volunteer.dtypes)

#*****************************************************************************#

#***************************Training and Test Sets****************************#

#Stratified sampling#

# Create a data with all columns except category_desc
volunteer_X = volunteer.drop('category_desc', axis=1)

# Create a category_desc labels dataset
volunteer_y = volunteer[['category_desc']]

# Use stratified sampling to split up the dataset according to the volunteer_y dataset
X_train, X_test, y_train, y_test = train_test_split(volunteer_X, volunteer_y, stratify=volunteer_y)

# Print out the category_desc counts on the training y labels
print(y_train['category_desc'].value_counts())

#*****************************************************************************#

#*****************************************************************************#