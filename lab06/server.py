import socket
import random
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# Generate DH key pair
def generate_private_key(p):
    return random.randint(2, p - 2)

def generate_public_key(private_key, g, p):
    return pow(g, private_key, p)

def compute_shared_secret(received_public_key, private_key, p):
    return pow(received_public_key, private_key, p)

def encrypt(plaintext, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return iv + ciphertext

def decrypt(ciphertext, key):
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext

# Prime number (p) and primitive root (g)
p = 23
g = 5

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(2)
print("Server is listening...")

conn, addr = server.accept()
print(f"Connection from {addr} has been established.")

# Server generates DH key pair
server_private_key = generate_private_key(p)
server_public_key = generate_public_key(server_private_key, g, p)

# Send server public key to client
conn.sendall(str(server_public_key).encode())

# Receive client public key
client_public_key = int(conn.recv(1024).decode())

# Compute shared secret
shared_secret = compute_shared_secret(client_public_key, server_private_key, p)
shared_secret_hash = hashlib.sha256(str(shared_secret).encode()).digest()
aes_key = shared_secret_hash[:32]

#Hidden pirate connection
conn2, addr2 = server.accept()

# Communicate securely using AES
while True:
    ciphertext = conn.recv(1024)
    if not ciphertext:
        break
    #print(f"Encrypted Text: {ciphertext}")
    decrypted_message = decrypt(ciphertext, aes_key)
    print(f"Client: {decrypted_message.decode()}")

    response = input("Server: ")
    encrypted_response = encrypt(response.encode(), aes_key)
    conn.sendall(encrypted_response)

    #Dummy Pirate
    conn2.sendall(encrypted_response)

conn.close()
server.close()
