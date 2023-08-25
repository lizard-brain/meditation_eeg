import pandas as pd
from scipy import integrate
import os
import matplotlib.pyplot as plt

def generate_auc_graph(data_path, interval=60):
    """
    Generate a graph showing the total area under the curve (AUC) for EEG metrics grouped by type.

    Parameters:
    - data_path (str): Path to the CSV file containing the EEG data.
    - interval (int): Interval in seconds for calculating AUC within.

    Returns:
    None
    """
    # Read the data
    data = pd.read_csv(data_path, delimiter=',')

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
    reference_time = data['TimeStamp'].min()
    data['TimeInSeconds'] = (data['TimeStamp'] - reference_time).dt.total_seconds()

    # Calculate AUC for each metric within specified intervals
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

    # Define metric groups
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

    # Define colors for each metric type
    metric_colors = {
        'Delta': 'red',
        'Theta': 'purple',
        'Alpha': 'blue',
        'Beta': 'green',
        'Gamma': 'orange'
    }

    # Create a bar chart for grouped AUC results
    plt.figure(figsize=(10, 6), facecolor='black')
    plt.rcParams['axes.facecolor'] = 'black'
    for metric_type, auc_values in grouped_results.items():
        plt.plot(range(len(auc_values)), auc_values, label=metric_type, color=metric_colors[metric_type], linewidth=4)
    plt.xlabel('Interval')
    plt.ylabel('Total Area Under the Curve (AUC)')
    plt.title('Total AUC for EEG Metrics Grouped by Type', color='white')
    legend = plt.legend()
    plt.setp(legend.get_texts(), color='white')
    plt.tight_layout()

    # Set the color of axis labels and tick labels to white
    plt.gca().xaxis.label.set_color('white')
    plt.gca().yaxis.label.set_color('white')
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')

    # Save the line chart as an image
    output_filename = os.path.splitext(os.path.basename(data_path))[0] + '_grouped_auc_line_chart.png'
    plt.savefig(output_filename, facecolor='black')

    # Display the line chart
    plt.show()

# Call the function with the data path and desired interval
generate_auc_graph('data.csv', interval=60)
