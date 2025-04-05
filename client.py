import socket
from threading import Thread
import os
from tkinter import messagebox
import time
import json

import globe

class Client:
    def __init__(self, HOST, PORT):
        self.socket = socket.socket()
        try:
            self.socket.connect((HOST, PORT))
            print("Connected to server")
        except:
            messagebox.showwarning("404 - Server not found", "You were unable to connect to a server.\nRefute mode is turned off.")
    
    def talk_to_server(self):
        self.socket.send(self.name.encode())
        Thread(target=self.receive_message).start()
        self.send_message()

    def send_message(self):
        while True:
            # Get user input
            client_input = input("Enter message: ")
            
            # Get the current timestamp
            timestamp = time.strftime('%b %d, %Y %I:%M %p')
            
            # Create a message dictionary to hold the necessary information
            message_dict = {
                "name_of_sender": self.name,
                "time_sent": timestamp,
                "message": client_input
            }
            
            # Convert to a JSON string
            json_message = json.dumps(message_dict)
            
            # Print the message being sent
            print(f"Sending message: {json_message}")
            
            # Send the JSON message
            self.socket.send(json_message.encode())

    def send_m(self, m: str) -> None:
        timestamp = time.strftime('%b %d, %Y %I:%M %p')
        client_message = f" {self.name}: {m}" 
        print(f"Sending message: {client_message}")  
        self.socket.send(client_message.encode())
    
    def set_name(self, name):
        self.name = name
        self.socket.send(self.name.encode())

    def receive_message(self):
        while True:
            server_message = self.socket.recv(1024).decode()
            
            if not server_message.strip():
                print("Server disconnected.")
                os._exit(0)

            # Print the message received from the server
            print(f"Received message: {server_message}")

            # Parse the received JSON message
            try:
                message_dict = json.loads(server_message)
                
                sender = message_dict["name_of_sender"]
                timestamp = message_dict["time_sent"]
                message = message_dict["message"]
                
                
                # Display 
                formatted_timestamp = f"{timestamp} \n {message}"
                globe.conversation.add_message(formatted_timestamp, align_right=False)
                
            
            except json.JSONDecodeError:
                print("Failed to decode message.")
                continue

if __name__ == "__main__":
    client = Client('127.0.0.1', 7633)
    client.name = input("Enter your name: ")  
    client.talk_to_server()
