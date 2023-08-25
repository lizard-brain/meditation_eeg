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

# Create separate subplots for each sensor's metrics
num_sensors = 4
fig, axs = plt.subplots(num_sensors, 1, figsize=(10, 6 * num_sensors))

sensors = ['TP9', 'AF7', 'AF8', 'TP10']
for i, sensor in enumerate(sensors):
    sensor_metrics = [metric for metric in metric_columns if sensor in metric]
    sensor_results = {metric: results[metric] for metric in sensor_metrics}

    axs[i].barh(list(sensor_results.keys()), list(sensor_results.values()), color='skyblue')
    axs[i].set_xlabel('Area Under the Curve (AUC)')
    axs[i].set_ylabel('Metrics')
    axs[i].set_title(f'AUC for {sensor} Metrics')

plt.tight_layout()

# Save the subplots as an image
plt.savefig('auc_subplots.png')

# Display the subplots
plt.show()
