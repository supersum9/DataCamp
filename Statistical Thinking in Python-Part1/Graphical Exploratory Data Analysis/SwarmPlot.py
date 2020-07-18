# Create bee swarm plot with Seaborn's default settings
_ = sns.swarmplot(x= 'species', y= 'petal length (cm)', data= df)

# Label the axes
plt.xlabel('Species')
plt.ylabel('Petal Lenght')
# Show the plot

plt.show()
