import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
import re
from ast import literal_eval

# Initialize the plot
fig, ax = plt.subplots()
x_data, y1_data, y2_data = [], [], []

# File path for continuously updated sensor data
file_path = "received_messages.txt"

# Maximum number of points to display on the plot
MAX_POINTS = 2000

# Function to read new lines from the file
def read_new_lines(file_path, last_position):
    with open(file_path, "r") as f:
        f.seek(last_position)
        lines = f.readlines()
        new_position = f.tell()
    return lines, new_position

# Initialize the last position of the file
last_position = 0

# Update function for animation
def update_plot(frame):
    global last_position

    # Read the new lines from the file
    new_lines, last_position = read_new_lines(file_path, last_position)

    # Process the new lines and update the plot data
    for line in new_lines:
        try:
            # Split the timestamp and list using regex
            timestamp_str, list_str = re.split(r' \[', line)
            list_str = '[' + list_str  # Add back the opening bracket

            # Convert the string to a list
            numeric_list = literal_eval(list_str)

            # Convert timestamp to datetime object
            timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

            # Extract sensor values
            sensor_values = numeric_list  # Already in list format

            # Extract first two sensor values
            sensor1, sensor2 = sensor_values[0], sensor_values[1]

            # Append new data
            x_data.append(timestamp)
            y1_data.append(sensor1)
            y2_data.append(sensor2)

            # Keep only the last MAX_POINTS points
            if len(x_data) > MAX_POINTS:
                x_data.pop(0)
                y1_data.pop(0)
                y2_data.pop(0)

        except (ValueError, SyntaxError):
            # Ignore invalid lines
            continue

    # Clear the axis and re-plot
    ax.clear()
    ax.plot(x_data, y1_data, "r-", label="Sensor 1")
    ax.plot(x_data, y2_data, "b-", label="Sensor 2")
    
    ax.set_title("Real-time Sensor Data")
    ax.set_xlabel("Time")
    ax.set_ylabel("Sensor Values")
    ax.legend()
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%H:%M:%S"))  # Format time axis

# Create the animation object
ani = animation.FuncAnimation(fig, update_plot, interval=1000)  # Update every 1000ms

# Display the plot
plt.show()
