# Create box plot with Seaborn's default settings
_= sns.boxplot(x= 'species', y= 'petal length (cm)', data= df)

# Label the axes
_= plt.xlabel('Species')
_= plt.ylabel('Petal Length(cm)')

# Show the plot
plt.show()
