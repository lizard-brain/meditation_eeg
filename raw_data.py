import pandas as pd
import matplotlib.pyplot as plt

# Load the data from a CSV file or other source
# Replace 'data.csv' with the actual path to your data file
data = pd.read_csv('data.csv')

# Convert the TimeStamp column to a datetime format
# We use 'infer_datetime_format=True' to automatically detect the format
data['TimeStamp'] = pd.to_datetime(data['TimeStamp'], infer_datetime_format=True)

# Create subplots for all plots
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12, 18))

# Plot EEG sensor readings over time
for electrode in ['RAW_TP9', 'RAW_AF7', 'RAW_AF8', 'RAW_TP10']:
    axes[0].plot(data['TimeStamp'], data[electrode], label=electrode)
axes[0].set_xlabel('Time')
axes[0].set_ylabel('EEG Sensor Reading')
axes[0].set_title('EEG Sensor Readings over Time')
axes[0].legend()
axes[0].tick_params(axis='x', rotation=45)

# Plot brainwave frequencies over time
for freq_band in ['Delta_TP9', 'Theta_TP9', 'Alpha_TP9', 'Beta_TP9', 'Gamma_TP9']:
    axes[1].plot(data['TimeStamp'], data[freq_band], label=freq_band)
axes[1].set_xlabel('Time')
axes[1].set_ylabel('Brainwave Frequency')
axes[1].set_title('Brainwave Frequencies over Time')
axes[1].legend()
axes[1].tick_params(axis='x', rotation=45)

# Plot accelerometer and gyroscope data
for sensor in ['Accelerometer_X', 'Accelerometer_Y', 'Accelerometer_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z']:
    axes[2].plot(data['TimeStamp'], data[sensor], label=sensor)
axes[2].set_xlabel('Time')
axes[2].set_ylabel('Sensor Reading')
axes[2].set_title('Accelerometer and Gyroscope Data over Time')
axes[2].legend()
axes[2].tick_params(axis='x', rotation=45)

# Adjust layout and display the plots
plt.tight_layout()
plt.show()
