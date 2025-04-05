import socket
from threading import Thread
import os

class Client:
    def __init__(self, HOST, PORT):
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))
        ##self.name = input("Enter your name: ")  # Fixed typo "imput" to "input"
        ##self.talk_to_server()

    def talk_to_server(self):
        self.socket.send(self.name.encode())
        Thread(target=self.receive_message).start()
        self.send_message()

    def send_message(self):
        while True:
            client_input = input("")
            client_message = self.name + ": " + client_input  # Added space after ":"
            self.socket.send(client_message.encode())

    def send_m(self, m:str) -> None:
        client_message = self.name + ": " + m  # Added space after ":"
        self.socket.send(client_message.encode())
    
    def set_name(self, name):
        self.name = name
        self.socket.send(self.name.encode())

    def receive_message(self):
        while True:
            server_message = self.socket.recv(1024).decode()
            if not server_message.strip():
                os._exit(0)
            print(server_message)  # Added to print the received message

if __name__ == "__main__":
    client = Client('127.0.0.1', 7633)
    client.name = input("Enter your name: ")  # Fixed typo "imput" to "input"
    client.talk_to_server()
