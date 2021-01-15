#*********************************Introducing Grid Search*********************#

#Build Grid Search functions#

# Create the function
def gbm_grid_search(learn_rate, max_depth):

	# Create the model
    model = GradientBoostingClassifier(learning_rate=learn_rate,\
        max_depth=max_depth)

    # Use the model to make predictions
    predictions = model.fit(X_train, y_train).predict(X_test)

    # Return the hyperparameters and score
    return([learn_rate, max_depth, accuracy_score(y_test, predictions)])

#*****************************************************************************#

#Iteratively tune multiple hyperparameters#

results_list = []
learn_rate_list = [0.01, 0.1, 0.5]
max_depth_list = [2,4,6]

# Extend the function input
def gbm_grid_search_extended(learn_rate, max_depth, subsample):

	# Extend the model creation section
    model = GradientBoostingClassifier(learning_rate=learn_rate, \
        max_depth=max_depth, subsample=subsample)

    predictions = model.fit(X_train, y_train).predict(X_test)

    # Extend the return part
    return([learn_rate, max_depth, subsample, \
        accuracy_score(y_test, predictions)])

#*****************************************************************************#

results_list = []

# Create the new list to test
subsample_list = [0.4, 0.6]

for learn_rate in learn_rate_list:
    for max_depth in max_depth_list:

    	# Extend the for loop
        for subsample in subsample_list:

            # Extend the results to include the new hyperparameter
            results_list.append(gbm_grid_search_extended\
                (learn_rate, max_depth, subsample))

# Print results
print(results_list)

#*****************************************************************************#

#**********************Grid Search with Scikit Learn**************************#

#GridSearchCV with Scikit Learn#

# Create a Random Forest Classifier with specified criterion
rf_class = RandomForestClassifier(criterion= 'entropy')

# Create the parameter grid
param_grid = {'max_depth': [2, 4, 8, 15], 'max_features': ['auto', 'sqrt']}

# Create a GridSearchCV object
grid_rf_class = GridSearchCV(
    estimator=rf_class,
    param_grid=param_grid,
    scoring='roc_auc',
    n_jobs=4,
    cv=5,
    refit=True, return_train_score=True)
print(grid_rf_class)

#*****************************************************************************#

#********************Understanding a grid search output***********************#

#Exploring the grid search results#

# Read the cv_results property into a dataframe & print it out
cv_results_df = pd.DataFrame(grid_rf_class.cv_results_)
print(cv_results_df)

# Extract and print the column with a dictionary of hyperparameters used
column = cv_results_df.loc[:, ['params']]
print(column)

# Extract and print the row that had the best mean test score
best_row = cv_results_df[cv_results_df['rank_test_score'] == 1 ]
print(best_row)

#*****************************************************************************#

#Analyzing the best results#

# Print out the ROC_AUC score from the best-performing square
best_score = grid_rf_class.best_score_
print(best_score)

# Create a variable from the row related to the best-performing square
cv_results_df = pd.DataFrame(grid_rf_class.cv_results_)
best_row = cv_results_df.loc[[grid_rf_class.best_index_]]
print(best_row)

# Get the n_estimators parameter from the best-performing square and print
best_n_estimators = grid_rf_class.best_params_["n_estimators"]
print(best_n_estimators)

#*****************************************************************************#

#Using the best results#

# See what type of object the best_estimator_ property is
print(type(grid_rf_class.best_estimator_))

# Create an array of predictions directly using the best_estimator_ property
predictions = grid_rf_class.best_estimator_.predict(X_test)

# Take a look to confirm it worked, this should be an array of 1's and 0's
print(predictions[0:5])

# Now create a confusion matrix
print("Confusion Matrix \n", confusion_matrix(y_test, predictions))

# Get the ROC-AUC score
predictions_proba = grid_rf_class.best_estimator_.predict_proba(X_test)[:,1]
print("ROC-AUC Score \n", roc_auc_score(y_test, predictions_proba))

#*****************************************************************************#