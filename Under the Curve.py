import pandas as pd
import numpy as np
from scipy import integrate

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



'''
# Remove rows with extreme values (considering a simple threshold for this example)
threshold = 10  # Adjust this threshold as needed
data = data[(data.iloc[:, 1:] < threshold).all(axis=1)]
'''


# Save the cleaned data to a new CSV file
cleaned_file_path = 'cleaned_data.csv'
data.to_csv(cleaned_file_path, index=False)
print(f"Cleaned data saved to '{cleaned_file_path}'")


# Calculate AUC for each metric
results = {}
for metric in metric_columns:
    try:
        auc = integrate.simps(data[metric], data['TimeStamp'])
        results[metric] = auc
    except KeyError as e:
        print(f"Error: {e} not found in the data.")

# Print the AUC results
for metric, auc in results.items():
    print(f'AUC for {metric}: {auc}')

# Optionally, you can save the results to a CSV file
results_df = pd.DataFrame(results, index=[0])
results_df.to_csv('auc_results.csv', index=False)
