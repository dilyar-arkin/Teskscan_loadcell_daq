#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#define NUM_SENSORS 4

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };  // MAC address
IPAddress ip(192, 168, 1, 177);  // Arduino static IP
IPAddress computerIP(192, 168, 1, 100);  // Computer's IP address
unsigned int localPort = 8888;  // Local port to listen on

EthernetUDP Udp;

const int addressPins[4] = {26, 28, 30, 32};  // Digital pins for binary addressing
int sensorData[NUM_SENSORS];              // Array to store sensor readings

// Lookup table for 4-bit binary addressing
const int sensorAddresses[NUM_SENSORS][4] = {
  {LOW, LOW, LOW, LOW},   // 0000 - Sensor 0
  {HIGH, LOW, LOW, LOW},  // 0001 - Sensor 1
  {LOW, HIGH, LOW, LOW},  // 0010 - Sensor 2
  {HIGH, HIGH, LOW, LOW}  // 0011 - Sensor 3
};

void setup() {
  for (int i = 0; i < 4; i++) {
    pinMode(addressPins[i], OUTPUT);
    Serial.println("setup digital pin to output");
  }
  Serial.begin(9600);

  // Start the Ethernet
  Ethernet.begin(mac, ip);

  // Check Ethernet hardware
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet shield was not found.");
    //while (true);  // Stop execution
  }

  // Check if the Ethernet cable is connected
  if (Ethernet.linkStatus() == LinkOFF) {
    Serial.println("Ethernet cable is not connected.");
    delay(10);
  } else {
    Serial.println("Ethernet connected successfully!");
    delay(10);
  }

  // Start UDP
  Udp.begin(localPort);

}

void setSensorAddress(int sensorID) {

  // Set digital pins based on the lookup table
  for (int i = 0; i < 4; i++) {
    
    digitalWrite(addressPins[i], sensorAddresses[sensorID][i]);
    //Serial.println(String(i) + ", "+ String(sensorAddresses[sensorID][i]));
  }
  //Serial.println("end of sensor" );
}

void acquireAnalogData() {
  for (int i = 0; i < NUM_SENSORS; i++) {
    setSensorAddress(i);  // Set sensor address from LUT
    delay(50);            // Small delay to allow sensor switching
    sensorData[i] = analogRead(A0);
    delay(50);
    //Serial.println(String(sensorData[0]));
  }
}

void sendDataToEthernet() {
  char message[50];  // Buffer to store the formatted message
  int index = 0;

  index += snprintf(message + index, sizeof(message) - index, "["); // Start array format

  for (int i = 0; i < NUM_SENSORS; i++) {
    index += snprintf(message + index, sizeof(message) - index, "%d", sensorData[i]);
    if (i < NUM_SENSORS - 1) {
      index += snprintf(message + index, sizeof(message) - index, ", ");
    }
  }

  snprintf(message + index, sizeof(message) - index, "]"); // Close the array format

  Serial.println(message);  // Print the message for debugging

  if (Udp.beginPacket(computerIP, localPort)) {
    Udp.write(message);  // Directly send the character array
    //delay(20);
    Udp.endPacket();
    //Serial.println("Sent UDP Packet: " + String(message)); // Convert to String for Serial output
  } else {
    Serial.println("Failed to send UDP packet");
  }
}


void loop() {
  
  acquireAnalogData();
  sendDataToEthernet();
  delay(50);  // Wait for 50 milliseconds before sending the next reading
}
