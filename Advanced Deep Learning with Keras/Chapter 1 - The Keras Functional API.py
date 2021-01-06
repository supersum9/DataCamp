#*****************************Keras input and dense layers********************#

#Input layers#

# Import Input from keras.layers
from keras.layers import Input

# Create an input layer of shape 1
input_tensor = Input(shape=(1,))

#*****************************************************************************#

#Dense layers#

# Load layers
from keras.layers import Input, Dense

# Input layer
input_tensor = Input(shape=(1,))

# Dense layer
output_layer = Dense(1)

# Connect the dense layer to the input_tensor
output_tensor = output_layer(input_tensor)

#*****************************************************************************#

#Output layers#

# Load layers
from keras.layers import Input, Dense

# Input layer
input_tensor = Input(shape=(1,))

# Create a dense layer and connect the dense layer to the input_tensor in one step
# Note that we did this in 2 steps in the previous exercise, but are doing it in one step now
output_tensor = Dense(1)(input_tensor)

#*****************************************************************************#

#*************************Build and compile a model***************************#

#Build a model#

# Input/dense/output layers
from keras.layers import Input, Dense
input_tensor = Input(shape=(1,))
output_tensor = Dense(1)(input_tensor)

# Build the model
from keras.models import Model
model = Model(input_tensor, output_tensor)

#*****************************************************************************#

#Compile a model#

# Compile the model
model.compile(optimizer='adam', loss='mean_absolute_error')

#*****************************************************************************#

#Visualize a model#

# Import the plotting function
from keras.utils import plot_model
import matplotlib.pyplot as plt

# Summarize the model
model.summary()

# Plot the model
plot_model(model, to_file='model.png')

# Display the image
data = plt.imread('model.png')
plt.imshow(data)
plt.show()

#*****************************************************************************#

#**************************Fit and evaluate a model***************************#

#Fit the model to the tournament basketball data#

# Now fit the model
model.fit(games_tourney_train['seed_diff'], games_tourney_train['score_diff'],
          epochs= 1,
          batch_size= 128,
          validation_split= 0.1,
          verbose=True)

#*****************************************************************************#

#Evaluate the model on a test set#

# Load the X variable from the test data
X_test = games_tourney_test['seed_diff']

# Load the y variable from the test data
y_test = games_tourney_test.score_diff

# Evaluate the model on the test data
print(model.evaluate(X_test, y_test, verbose=False))

#*****************************************************************************#