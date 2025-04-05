import socket
from threading import Thread
import time
import json

class Server:
    rooms = {}  # Dictionary to store rooms and their clients

    def __init__(self, HOST, PORT):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(5)
        print('Server waiting for connection...')

    def listen(self):
        while True:
            client_socket, address = self.server_socket.accept()
            print("Connection from " + str(address))

            client_name = client_socket.recv(1024).decode()
            room_id = self.get_room_for_client()
            client = {"client_name": client_name, 'client_socket': client_socket, 'room_id': room_id}
            
            # Add client to the room
            if room_id not in Server.rooms:
                Server.rooms[room_id] = []
            Server.rooms[room_id].append(client)
            
            # Broadcast to others in the same room that a new client has joined
            self.broadcast_message(client_name, client_name + " has joined the room", room_id)

            # Start a new thread to handle this client
            Thread(target=self.handle_new_client, args=(client,)).start()

    def get_room_for_client(self):
        # Check if there is an available room with less than 2 clients
        for room_id, clients in Server.rooms.items():
            if len(clients) < 2:
                return room_id
        # If not, create a new room
        new_room_id = len(Server.rooms) + 1
        return str(new_room_id)

    def handle_new_client(self, client):
        client_name = client['client_name']
        client_socket = client['client_socket']
        room_id = client['room_id']

        while True:
            try:
                # Receive the message from the client
                client_message = client_socket.recv(1024).decode()

                # If the message is "bye" or empty, disconnect the client
                if client_message.strip() == client_name + ": bye" or not client_message.strip():
                    self.broadcast_message(client_name, client_name + " has left the room", room_id)
                    Server.rooms[room_id].remove(client)
                    client_socket.close()
                    break
                else:
                    # Broadcast the message to others in the same room
                    self.broadcast_message(client_name, client_message, room_id)

            except Exception as e:
                print(f"Error handling client {client_name}: {e}")
                break

    def broadcast_message(self, sender_name, message, room_id):
        for client in Server.rooms[room_id]:
            client_socket = client['client_socket']
            if client['client_name'] != sender_name:
                try:
                    # Adding timestamp
                    timestamp = time.strftime('%b %d, %Y %I:%M %p')
                    message_dict = {
                        "name_of_sender": sender_name,
                        "time_sent": timestamp,
                        "message": message
                    }
                    
                    # Convert the message to JSON and send it
                    json_message = json.dumps(message_dict)
                    client_socket.send(json_message.encode())

                except Exception as e:
                    print(f"Error sending message to {client['client_name']}: {e}")
                    continue

if __name__ == '__main__':
    server = Server('127.0.0.1', 7633)
    server.listen()
