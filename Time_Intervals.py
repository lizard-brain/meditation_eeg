import pandas as pd
from scipy import integrate
from datetime import datetime, timedelta
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

# Convert 'TimeStamp' to seconds since a reference point
reference_time = data['TimeStamp'].min()  # Choose a reference time
data['TimeInSeconds'] = (data['TimeStamp'] - reference_time).dt.total_seconds()

# Calculate AUC for each metric within 2-minute intervals
interval = 60  # 2 minutes in seconds
results = {}
for metric in metric_columns:
    try:
        auc_values = []
        for start_time in range(0, int(data['TimeInSeconds'].max()), interval):
            interval_data = data[(data['TimeInSeconds'] >= start_time) &
                                 (data['TimeInSeconds'] < start_time + interval)]
            if not interval_data.empty:
                auc = integrate.simps(interval_data[metric], interval_data['TimeInSeconds'])
                auc_values.append(auc)
        results[metric] = auc_values
    except KeyError as e:
        print(f"Error: {e} not found in the data.")

# Create a dictionary to group metrics by type (same as before)
metric_groups = {
    'Delta': ['Delta_TP9', 'Delta_AF7', 'Delta_AF8', 'Delta_TP10'],
    'Theta': ['Theta_TP9', 'Theta_AF7', 'Theta_AF8', 'Theta_TP10'],
    'Alpha': ['Alpha_TP9', 'Alpha_AF7', 'Alpha_AF8', 'Alpha_TP10'],
    'Beta': ['Beta_TP9', 'Beta_AF7', 'Beta_AF8', 'Beta_TP10'],
    'Gamma': ['Gamma_TP9', 'Gamma_AF7', 'Gamma_AF8', 'Gamma_TP10']
}

# Aggregate AUC values by metric type for each interval
grouped_results = {metric_type: [sum(results[metric][i] for metric in metrics)
                                  for i in range(len(results[metric]))]
                   for metric_type, metrics in metric_groups.items()}

# Create a bar chart for grouped AUC results
plt.figure(figsize=(10, 6))
for metric_type, auc_values in grouped_results.items():
    plt.plot(range(len(auc_values)), auc_values, label=metric_type)
plt.xlabel('Interval')
plt.ylabel('Total Area Under the Curve (AUC)')
plt.title('Total AUC for EEG Metrics Grouped by Type')
plt.legend()
plt.tight_layout()

# Save the line chart as an image
plt.savefig('grouped_auc_line_chart.png')

# Display the line chart
plt.show()
