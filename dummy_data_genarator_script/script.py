import pandas as pd
import numpy as np
import datetime

# Function to generate dummy data
def generate_dummy_data():
    # Define the start and end times
    start_time = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = start_time + datetime.timedelta(days=1)

    # Generate a list of timestamps for each second of the day
    timestamps = pd.date_range(start=start_time, end=end_time, freq='S')[:-1]

    # Generate random wattage data
    wattage = np.random.choice([0, np.random.uniform(10, 500)], size=len(timestamps), p=[0.1, 0.9])

    # Create a DataFrame
    data = pd.DataFrame({
        'TimeDate': timestamps,
        'Watt': wattage
    })

    return data

# Generate the data
dummy_data = generate_dummy_data()

# Save to a CSV file
dummy_data.to_csv('dummy_electricity_usage.csv', index=False)

print("Data saved to dummy_electricity_usage.csv")
