import socket
import threading

clients = []  # List to keep track of connected clients

def handle_client(client_socket, client_address):
    print(f"Connection established with {client_address}")
    while True:
        try:
            message = client_socket.recv(1024).decode()  # Receive message from client
            if message.lower() == 'bye':  # Disconnect condition
                print(f"{client_address} disconnected.")
                clients.remove(client_socket)
                client_socket.close()
                break

            # Relay the message to the other client
            for other_client in clients:
                if other_client != client_socket:
                    other_client.send(message.encode())
        except:
            print(f"Error with client {client_address}.")
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    host = '127.0.0.1'  # Localhost
    port = 5000         # Arbitrary port number

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)  # Listen for up to two clients
    print("Server is waiting for connections...")

    while len(clients) < 2:  # Accept up to two clients
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
