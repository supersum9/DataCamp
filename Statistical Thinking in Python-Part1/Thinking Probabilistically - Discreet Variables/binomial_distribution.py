# Take 10,000 samples out of the binomial distribution: n_defaults
n_defaults = np.random.binomial(n=100, p=0.05, size=10000)

# Compute CDF: x, y
x,y = ecdf(n_defaults)

# Plot the CDF with axis labels
_ = plt.plot(x, y, marker= '.', linestyle= 'none')
_ = plt.xlabel('Defaults')
_ = plt.ylabel('ECDF')

# Show the plot
plt.show()
