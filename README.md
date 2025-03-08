# Teskscan_loadcell_daq
Block cave mine simulator Tank 2 - DAQ setup


# Arduino Ethernet UDP Communication for Sensor Data

This project allows an Arduino to read data from multiple sensors and send it via UDP over an Ethernet connection. The Arduino collects sensor data from 4 different analog sensors, formats the data into an array, and transmits it to a computer over the network using UDP.

## Hardware Requirements

- Arduino Board (e.g., Arduino Uno)
- Ethernet Shield (compatible with Arduino)
- 4 Analog sensors connected to analog input pins
- Jumper wires for connecting sensors
- Ethernet cable for network connection
- A computer to receive the UDP data

## Software Requirements

- Arduino IDE
- Ethernet library
- EthernetUDP library

## Pin Configuration

- `addressPins[]`: Digital pins 26, 28, 30, and 32 are used for binary addressing of sensors.
- `sensorAddresses[][]`: A lookup table stores the binary sensor addresses for the 4 sensors.

## Circuit Setup

- Connect each sensor to an analog pin on the Arduino (A0 is used in the code).
- Ensure the Ethernet shield is connected to the Arduino and has an active Ethernet connection.

## Code Overview

### Setup
1. The Arduino initializes the Ethernet shield and assigns a static IP address.
2. The Ethernet shield is checked for hardware and cable connection.
3. A UDP instance is started on the specified local port.

### Main Functions
- **`setSensorAddress(int sensorID)`**: This function selects the correct sensor address using the `addressPins[]` and `sensorAddresses[][]` lookup table.
- **`acquireAnalogData()`**: Reads the analog data from each sensor.
- **`sendDataToEthernet()`**: Sends the acquired sensor data as a UDP packet to a specified computer IP.

### Loop
In the `loop()`, the code continuously reads data from the sensors and sends it via Ethernet as a UDP packet.

## Instructions

### Upload the Code
1. Open the Arduino IDE.
2. Copy and paste the `Source_code_arduino_send_via_ethernet.ino` code into the IDE.
3. Select the appropriate board and port in the IDE.
4. Upload the code to your Arduino.

### Configuration
- Update the `IPAddress` variables in the code to match your network setup:
  - `ip`: Arduino's static IP address.
  - `computerIP`: IP address of the receiving computer.
  - `localPort`: Local UDP port (default: `8888`).
  
### Monitoring
- Open the Serial Monitor in the Arduino IDE to view the debug output and ensure the Arduino is properly communicating over Ethernet.

### Network Communication
- The Arduino will send a UDP packet to the specified computer IP with the sensor data in the form of a JSON-like array.
- Example of transmitted data: [1023, 512, 356, 987]
  
## Troubleshooting
- Ensure the Ethernet shield is properly connected and the Ethernet cable is functional.
- Verify that the Arduino has the correct static IP and that the computer is listening on the correct port for incoming UDP packets.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


