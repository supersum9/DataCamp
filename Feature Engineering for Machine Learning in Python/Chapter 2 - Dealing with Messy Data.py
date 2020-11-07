#*************************Why do missing values exist?************************#

#How sparse is my data?#

# Subset the DataFrame
sub_df = so_survey_df[['Age','Gender']]

# Print the number of non-missing values
print(sub_df.notnull().sum())

#*****************************************************************************#

