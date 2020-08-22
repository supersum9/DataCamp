#****************************Left join********************************#

#Counting missing rows with left join#

# Merge the movies table with the financials table with a left join
movies_financials = movies.merge(financials, on='id', how='left')

# Count the number of rows in the budget column that are missing
number_of_missing_fin = movies_financials['budget'].isnull().sum()

# Print the number of movies missing financials
print(number_of_missing_fin)

#*********************************************************************#

#Enriching a dataset#

# Merge the toy_story and taglines tables with a left join
toystory_tag = toy_story.merge(taglines, on='id', how='left')

# Print the rows and shape of toystory_tag
print(toystory_tag)
print(toystory_tag.shape)

#*********************************************************************#

#**************************Other joins********************************#

#Right join to find unique movies#

# Merge action_movies to the scifi_movies with right join
action_scifi = action_movies.merge(scifi_movies, on='movie_id', how='right',
                                   suffixes=('_act','_sci'))

# From action_scifi, select only the rows where the genre_act column is null
scifi_only = action_scifi[action_scifi['genre_act'].isnull()]

# Merge action_movies to the scifi_movies with right join
action_scifi = action_movies.merge(scifi_movies, on='movie_id', how='right',
                                   suffixes=('_act','_sci'))

# From action_scifi, select only the rows where the genre_act column is null
scifi_only = action_scifi[action_scifi['genre_act'].isnull()]

# Merge the movies and scifi_only tables with an inner join
movies_and_scifi_only = movies.merge(scifi_only, left_on='id', right_on='movie_id')

# Print the first few rows and shape of movies_and_scifi_only
print(movies_and_scifi_only.head())
print(movies_and_scifi_only.shape)

#*********************************************************************#

#Popular genres with right join#

# Use right join to merge the movie_to_genres and pop_movies tables
genres_movies = movie_to_genres.merge(pop_movies, how='right',
                                      left_on= 'movie_id',
                                      right_on= 'id')

# Count the number of genres
genre_count = genres_movies.groupby('genre').agg({'id':'count'})

# Plot a bar chart of the genre_count
genre_count.plot(kind='bar')
plt.show()

#*********************************************************************#

#Using outer join to select actors#

# Merge begins_actors to returns_actors on id with outer join using suffixes
begins_returns = begins_actors.merge(returns_actors,
                                     on='id',
                                     how='outer',
                                     suffixes=('_beg','_ret'))

# Create an index that returns true if name_beg or name_ret are null
m = ((begins_returns['name_beg'].isnull()) |
     (begins_returns['name_ret'].isnull()))

# Print the first few rows of begins_returns
print(begins_returns[m].head())

#*********************************************************************#

