import socket
from threading import Thread
import os
from tkinter import messagebox

import globe

class Client:
    def __init__(self, HOST, PORT):
        self.socket = socket.socket()
        try:
            self.socket.connect((HOST, PORT))
        except:
            messagebox.showwarning("404 - Server not found", "You were unable to connect to a server.\nRefute mode is turned off.")
        ##self.name = input("Enter your name: ") 
        ##self.talk_to_server()

    def talk_to_server(self):
        self.socket.send(self.name.encode())
        Thread(target=self.receive_message).start()
        self.send_message()

    def send_message(self):
        while True:
            client_input = input("")
            client_message = self.name + ": " + client_input  
            self.socket.send(client_message.encode())

    def send_m(self, m:str) -> None:
        client_message = self.name + ": " + m  
        self.socket.send(client_message.encode())
    
    def set_name(self, name):
        self.name = name
        self.socket.send(self.name.encode())

    def receive_message(self):
        while True:
            server_message = self.socket.recv(1024).decode()
            if not server_message.strip():
                os._exit(0)
            globe.conversation.add_message(server_message, align_right=False)

if __name__ == "__main__":
    client = Client('127.0.0.1', 7633)
    client.name = input("Enter your name: ")  
    client.talk_to_server()
