import socket
import os

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

print("Connected to server")

while True:
    ciphertext = client.recv(1024)
    if not ciphertext:
        break
    print(f"Listened message from server: {ciphertext}")

client.close()
