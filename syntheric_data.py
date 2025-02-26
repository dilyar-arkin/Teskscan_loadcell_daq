import time
import numpy as np

# The file path where the sinusoidal data will be saved
file_path = 'data.txt'

# Function to generate and append sinusoidal data to the file
def add_sinusoidal_data(file_path, amplitude=1, frequency=1, noise_level=0.1):
    x_value = 0  # Start at 0 for the x-values
    while True:
        # Generate y value as a sinusoidal function of x
        y_value = amplitude * np.sin(frequency * x_value) + np.random.normal(0, noise_level)

        # Format the new data as a string (x y)
        new_data = f"{x_value} {y_value}\n"

        # Append the new data to the file
        with open(file_path, 'a') as f:
            f.write(new_data)

        print(f"Added: {new_data.strip()}")  # Print the new data added to the file

        # Increment x_value for the next point (step size of 0.1)
        x_value += 0.1

        # Wait for a short period before adding more data (e.g., 0.1 second)
        time.sleep(0.1)

# Call the function to start adding sinusoidal data
add_sinusoidal_data(file_path)
