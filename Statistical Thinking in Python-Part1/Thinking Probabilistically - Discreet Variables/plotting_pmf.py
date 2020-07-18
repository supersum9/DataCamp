# Compute bin edges: bins
bins = np.arange(0, max(n_defaults) + 1.5) - 0.5

# Generate histogram
_ = plt.hist(n_defaults, normed= True, bins= bins)
plt.margins(0.02)
# Label axes
_ = plt.xlabel('Number of defaults per 100 loans')
_ = plt.ylabel('PMF')

# Show the plot
plt.show()