import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()  # Receive message from server
            print(f"Other Client: {message}")
        except:
            print("Disconnected from server.")
            client_socket.close()
            break

def start_client():
    host = '127.0.0.1'  # Localhost
    port = 5000         # Same port as the server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to the server!")

    # Start a thread to receive messages
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    while True:
        client_message = input("You: ")
        client_socket.send(client_message.encode())  # Send message to server
        if client_message.lower() == 'bye':  # Disconnect condition
            print("Disconnected from the server.")
            client_socket.close()
            break

if __name__ == "__main__":
    start_client()
