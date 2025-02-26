import socket
import datetime

def process_message(message, addr):
    """Process and store the received message with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"{timestamp} {message}"

    try:
        with open("received_messages.txt", "a") as file:
            file.write(formatted_message + "\n")
        print(f"Received message from {addr}: {formatted_message}")
    except IOError as e:
        print(f"Error writing to file: {e}")

def start_udp_server():
    """Start the UDP server to receive and process messages."""
    UDP_IP = "0.0.0.0"  # Listen on all available network interfaces
    UDP_PORT = 8888  # Same port as used in Arduino sketch

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(10)  # Set a timeout to prevent indefinite blocking
        sock.bind((UDP_IP, UDP_PORT))
        print(f"Listening on {UDP_IP}:{UDP_PORT}...")
    except socket.error as e:
        print(f"Socket error: {e}")
        return

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            try:
                message = data.decode().strip()
                process_message(message, addr)
            except UnicodeDecodeError:
                print(f"Received non-decodable message from {addr}")
        except socket.timeout:
            print("No data received within timeout period. Still listening...")
        except socket.error as e:
            print(f"Error receiving data: {e}")
        except KeyboardInterrupt:
            print("Server shutting down...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    sock.close()

if __name__ == "__main__":
    start_udp_server()
