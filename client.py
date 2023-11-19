import socket
import threading

# Define the server address and port
SERVER_ADDRESS = ('localhost', 8000)

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(SERVER_ADDRESS)

# Define a function to handle incoming messages
def handle_messages():
    while True:
        message = client_socket.recv(1024).decode()
        if not message:
            break
        print(f'Received message: {message}')

# Start a thread to handle incoming messages
thread = threading.Thread(target=handle_messages)
thread.start()

# Send messages to the server
while True:
    message = input('Enter message: ')
    client_socket.send(message.encode())
