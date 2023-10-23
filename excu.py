import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the Excel file using pandas
df = pd.read_excel('inpu.xlsx')  # Replace with the name of your Excel file
likes_data = df['NUMBER OF LIKES'].tolist()

# Create an array of x-coordinates (post indices)
x = range(1, len(likes_data) + 1)

# Plot the graph
plt.plot(x, likes_data)
plt.xlabel('Post Index')
plt.ylabel('Number of Likes')
plt.title('Number of Likes for Each Post')
plt.show()
