import pandas as pd
import matplotlib.pyplot as plt

# Load the data from a CSV file or other source
# Replace 'data.csv' with the actual path to your data file
data = pd.read_csv('data.csv')

# Convert the TimeStamp column to a datetime format
data['TimeStamp'] = pd.to_datetime(data['TimeStamp'], infer_datetime_format=True)

# Plot EEG sensor readings over time
plt.figure(figsize=(12, 6))
for electrode in ['RAW_TP9', 'RAW_AF7', 'RAW_AF8', 'RAW_TP10']:
    plt.plot(data['TimeStamp'], data[electrode], label=electrode)
plt.xlabel('Time')
plt.ylabel('EEG Sensor Reading')
plt.title('EEG Sensor Readings over Time')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot brainwave frequencies over time
plt.figure(figsize=(12, 6))
for freq_band in ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']:
    plt.plot(data['TimeStamp'], data[freq_band], label=freq_band)
plt.xlabel('Time')
plt.ylabel('Brainwave Frequency')
plt.title('Brainwave Frequencies over Time')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot accelerometer and gyroscope data
plt.figure(figsize=(12, 6))
for sensor in ['Accelerometer_X', 'Accelerometer_Y', 'Accelerometer_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z']:
    plt.plot(data['TimeStamp'], data[sensor], label=sensor)
plt.xlabel('Time')
plt.ylabel('Sensor Reading')
plt.title('Accelerometer and Gyroscope Data over Time')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
