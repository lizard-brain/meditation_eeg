import pandas as pd
import numpy as np
from scipy import integrate
from datetime import datetime
import matplotlib.pyplot as plt

# Read the data
data = pd.read_csv('data.csv', delimiter=',')

# Define the metric columns
metric_columns = ['Delta_TP9', 'Delta_AF7', 'Delta_AF8', 'Delta_TP10',
                  'Theta_TP9', 'Theta_AF7', 'Theta_AF8', 'Theta_TP10',
                  'Alpha_TP9', 'Alpha_AF7', 'Alpha_AF8', 'Alpha_TP10',
                  'Beta_TP9', 'Beta_AF7', 'Beta_AF8', 'Beta_TP10',
                  'Gamma_TP9', 'Gamma_AF7', 'Gamma_AF8', 'Gamma_TP10']

# Remove rows with missing values in any of the metric columns
data = data.dropna(subset=metric_columns)

# Convert 'TimeStamp' column to datetime
data['TimeStamp'] = pd.to_datetime(data['TimeStamp'])

# Convert 'TimeStamp' to seconds or milliseconds since a reference point
reference_time = data['TimeStamp'].min()  # Choose a reference time
data['TimeInSeconds'] = (data['TimeStamp'] - reference_time).dt.total_seconds()

# Calculate AUC for each metric
results = {}
for metric in metric_columns:
    try:
        auc = integrate.simps(data[metric], data['TimeInSeconds'])
        results[metric] = auc
    except KeyError as e:
        print(f"Error: {e} not found in the data.")

# Create a bar chart for AUC results
plt.figure(figsize=(10, 6))
plt.barh(list(results.keys()), list(results.values()), color='skyblue')
plt.xlabel('Area Under the Curve (AUC)')
plt.ylabel('Metrics')
plt.title('AUC for EEG Metrics')
plt.tight_layout()

# Save the bar chart as an image
plt.savefig('auc_bar_chart.png')

# Display the bar chart
plt.show()
