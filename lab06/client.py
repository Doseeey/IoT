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

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

# Client generates DH key pair
client_private_key = generate_private_key(p)
client_public_key = generate_public_key(client_private_key, g, p)

# Receive server public key
server_public_key = int(client.recv(1024).decode())

# Send client public key to server
client.sendall(str(client_public_key).encode())

# Compute shared secret
shared_secret = compute_shared_secret(server_public_key, client_private_key, p)
shared_secret_hash = hashlib.sha256(str(shared_secret).encode()).digest()
aes_key = shared_secret_hash[:32]

# Communicate securely using AES
while True:
    message = input("Client: ")
    encrypted_message = encrypt(message.encode(), aes_key)
    client.sendall(encrypted_message)

    ciphertext = client.recv(1024)
    if not ciphertext:
        break
    decrypted_response = decrypt(ciphertext, aes_key)
    print(f"Server: {decrypted_response.decode()}")

client.close()
