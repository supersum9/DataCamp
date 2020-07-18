# Draw samples of waiting times: waiting_times
waiting_times = successive_poisson(764, 715, size= 100000)

# Make the histogram
_ = plt.hist(waiting_times, bins=100, normed= True, histtype= 'step')


# Label axes
_ = plt.xlabel('Waiting Times')
_ = plt.ylabel('PDF')

# Show the plot
plt.show()
