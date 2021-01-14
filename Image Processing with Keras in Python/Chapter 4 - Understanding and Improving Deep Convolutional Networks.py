#****************************Tracking learning********************************#

#Plot the learning curves#

import matplotlib.pyplot as plt

# Train the model and store the training object
training = model.fit(train_data, train_labels, epochs=3, validation_split=0.2, \
        batch_size=10)

# Extract the history from the training object
history = training.history

# Plot the training loss
plt.plot(history['loss'])
# Plot the validation loss
plt.plot(history['val_loss'])

# Show the figure
plt.show()

#*****************************************************************************#

#Using stored weights to predict in a test set#

# Load the weights from file
model.load_weights('weights.hdf5')

# Predict from the first three images in the test data
model.predict(test_data[:3])

#*****************************************************************************#

#******************************Regularization*********************************#

#Adding dropout to your network#

# Add a convolutional layer
model.add(Conv2D(15, kernel_size=2, activation='relu',
                 input_shape=(img_rows, img_cols, 1)))

# Add a dropout layer
model.add(Dropout(0.20))

# Add another convolutional layer
model.add(Conv2D(5, kernel_size=2, activation='relu'))

# Flatten and feed to output layer
model.add(Flatten())
model.add(Dense(3, activation='softmax'))

#*****************************************************************************#

#Add batch normalization to your network#

# Add a convolutional layer
model.add(Conv2D(15, kernel_size=2, activation='relu',\
    input_shape=(img_cols,img_rows,1)))


# Add batch normalization layer
model.add(BatchNormalization())

# Add another convolutional layer
model.add(Conv2D(5, kernel_size=2, activation='relu'))

# Flatten and feed to output layer
model.add(Flatten())
model.add(Dense(3, activation='softmax'))

#*****************************************************************************#

#****************************Interpreting the model***************************#

#Extracting a kernel from a trained network#

# Load the weights into the model
model.load_weights('weights.hdf5')

# Get the first convolutional layer from the model
c1 = model.layers[0]

# Get the weights of the first convolutional layer
weights1 = c1.get_weights()

# Pull out the first channel of the first kernel in the first layer
kernel = weights1[0][...,0, 0]
print(kernel)

#*****************************************************************************#

#Visualizing kernel responses#

import matplotlib.pyplot as plt

# Convolve with the fourth image in test_data
out = convolution(test_data[3, :, :, 0], kernel)

# Visualize the result
plt.imshow(out)
plt.show()

#*****************************************************************************#