import matplotlib.pyplot as plt
import numpy as np

# Define the data as a numpy array
data = np.array([
    [3.2, 2.3],
    [4.7, 0.8],
    [3.29, 1.57],
    [8.72, 3.74],
    [30.8, 4.3],
    [3.41, 3.89],
])

# Define the labels for the x-axis (software project names)
labels = ['apm-agent-java', 'dubbo', 'fresco', 'netty',
          'okhttp','spring-framework']

# Compute the difference between the two columns
diff = data[:, 0] - data[:, 1]

# Define the colors for the bars
colors = np.where(diff > 0, '#54a021', '#f44336')

# Create a horizontal bar chart
plt.barh(y=range(len(labels)), width=diff, height=0.7, color=colors)
# for i, v in enumerate(diff):
#     plt.text(v, i, str(round(v, 2)), color='black', fontweight='bold', ha='left', va='center_baseline')

# Add the project names as labels to the y-axis
plt.yticks(range(len(labels)), labels)



# Add a title and labels to the x-axis
plt.title('Mean Density')
plt.xlabel('With Robustness Changes - Without Robustness Changes')

# Display the chart
plt.show()
