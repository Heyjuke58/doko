import socket
import threading
import time

# Define the server address and port
SERVER_ADDRESS = ('localhost', 8000)

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind(SERVER_ADDRESS)

# Listen for incoming connections
server_socket.listen(1)
print('Server is listening...')

# Create a list to store client sockets
client_sockets = []

# Define a function to handle incoming connections
def handle_connection(client_socket, client_address):
    print(f'New connection from {client_address}')
    client_sockets.append(client_socket)

    while True:
        # Receive message from client
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f'Received message: {message}')

            # Send message to all clients
            for socket in client_sockets:
                socket.send(message.encode())
        except:
            break

    # Close client socket
    client_socket.close()
    client_sockets.remove(client_socket)
    print(f'Connection closed with {client_address}')

# Accept incoming connections and spawn a new thread to handle each connection
while True:
    client_socket, client_address = server_socket.accept()
    thread = threading.Thread(target=handle_connection, args=(client_socket, client_address))
    thread.start()
