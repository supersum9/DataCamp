#****************************Pipeline*****************************************#

#Flight duration model: Pipeline stages#

# Convert categorical strings to index values
indexer = StringIndexer(inputCol= 'org', outputCol= 'org_idx')

# One-hot encode index values
onehot = OneHotEncoderEstimator(
    inputCols=['org_idx', 'dow'],
    outputCols=['org_dummy', 'dow_dummy']
)

# Assemble predictors into a single column
assembler = VectorAssembler(inputCols=['km', 'org_dummy', 'dow_dummy'], \
    outputCol='features')

# A linear regression object
regression = LinearRegression(labelCol= 'duration')

#*****************************************************************************#

#Flight duration model: Pipeline model#

# Import class for creating a pipeline
from pyspark.ml import Pipeline

# Construct a pipeline
pipeline = Pipeline(stages=[indexer, onehot, assembler, regression])

# Train the pipeline on the training data
pipeline = pipeline.fit(flights_train)

# Make predictions on the testing data
predictions = pipeline.transform(flights_test)

#*****************************************************************************#

#SMS spam pipeline#

from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF

# Break text into tokens at non-word characters
tokenizer = Tokenizer(inputCol='text', outputCol='words')

# Remove stop words
remover = StopWordsRemover(inputCol= tokenizer.getOutputCol(), outputCol='terms')

# Apply the hashing trick and transform to TF-IDF
hasher = HashingTF(inputCol= remover.getOutputCol(), outputCol="hash")
idf = IDF(inputCol= hasher.getOutputCol(), outputCol="features")

# Create a logistic regression object and add everything to a pipeline
logistic = LogisticRegression()
pipeline = Pipeline(stages=[tokenizer, remover, hasher, idf, logistic])

#*****************************************************************************#

#**************************Cross-Validation***********************************#

#Cross validating simple flight duration model#

# Create an empty parameter grid
params = ParamGridBuilder().build()

# Create objects for building and evaluating a regression model
regression = LinearRegression(labelCol= 'duration')
evaluator = RegressionEvaluator(labelCol= 'duration')

# Create a cross validator
cv = CrossValidator(estimator= regression, estimatorParamMaps= params, \
    evaluator= evaluator, numFolds= 5)

# Train and test model on multiple folds of the training data
cv = cv.fit(flights_train)

# NOTE: Since cross-valdiation builds multiple models, the fit()
# method can take a little while to complete.

#*****************************************************************************#

#Cross validating flight duration model pipeline#

# Create an indexer for the org field
indexer = StringIndexer(inputCol= 'org', outputCol= 'org_idx')

# Create an one-hot encoder for the indexed org field
onehot = OneHotEncoderEstimator(inputCols= ['org_idx'], outputCols= ['org_dummy'])

# Assemble the km and one-hot encoded fields
assembler = VectorAssembler(inputCols= ['km', 'org_dummy'], outputCol= 'features')

# Create a pipeline and cross-validator.
pipeline = Pipeline(stages=[indexer, onehot, assembler, regression])
cv = CrossValidator(estimator=pipeline,
          estimatorParamMaps=params,
          evaluator=evaluator)

#*****************************************************************************#

#*****************************Grid Search*************************************#

#Optimizing flights linear regression#

# Create parameter grid
params = ParamGridBuilder()

# Add grids for two parameters
params = params.addGrid(regression.regParam, [0.01, 0.1, 1.0, 10.0]) \
               .addGrid(regression.elasticNetParam, [0.0, 0.5, 1.0])

# Build the parameter grid
params = params.build()
print('Number of models to be tested: ', len(params))

# Create cross-validator
cv = CrossValidator(estimator=pipeline, \
                    estimatorParamMaps=params, \
                    evaluator=evaluator, \
                    numFolds= 5)

#*****************************************************************************#

#Dissecting the best flight duration model#

# Get the best model from cross validation
best_model = cv.bestModel

# Look at the stages in the best model
print(best_model.stages)

# Get the parameters for the LinearRegression object in the best model
best_model.stages[3].extractParamMap()

# Generate predictions on testing data using the best model then calculate RMSE
predictions = best_model.transform(flights_test)
evaluator.evaluate(predictions)

#*****************************************************************************#

#SMS spam optimised#

# Create parameter grid
params = ParamGridBuilder()

# Add grid for hashing trick parameters
params = params.addGrid(hasher.numFeatures, [1024, 4096, 16384]) \
               .addGrid(hasher.binary, [True, False])

# Add grid for logistic regression parameters
params = params.addGrid(logistic.regParam, [0.01, 0.1, 1.0, 10]) \
               .addGrid(logistic.elasticNetParam, [0.0, 0.5, 1.0])

# Build parameter grid
params = params.build()

#*****************************************************************************#

#*******************************Ensemble**************************************#

