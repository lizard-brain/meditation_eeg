import pandas as pd
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

# Create a dictionary to group metrics by type
metric_groups = {
    'Delta': ['Delta_TP9', 'Delta_AF7', 'Delta_AF8', 'Delta_TP10'],
    'Theta': ['Theta_TP9', 'Theta_AF7', 'Theta_AF8', 'Theta_TP10'],
    'Alpha': ['Alpha_TP9', 'Alpha_AF7', 'Alpha_AF8', 'Alpha_TP10'],
    'Beta': ['Beta_TP9', 'Beta_AF7', 'Beta_AF8', 'Beta_TP10'],
    'Gamma': ['Gamma_TP9', 'Gamma_AF7', 'Gamma_AF8', 'Gamma_TP10']
}

# Aggregate AUC values by metric type
grouped_results = {metric_type: sum(results[metric] for metric in metrics)
                   for metric_type, metrics in metric_groups.items()}

# Create a bar chart for grouped AUC results
plt.figure(figsize=(10, 6))
plt.barh(list(grouped_results.keys()), list(grouped_results.values()), color='skyblue')
plt.xlabel('Total Area Under the Curve (AUC)')
plt.ylabel('Metric Type')
plt.title('Total AUC for EEG Metrics Grouped by Type')
plt.tight_layout()

# Save the bar chart as an image
plt.savefig('grouped_auc_bar_chart.png')

# Display the bar chart
plt.show()
