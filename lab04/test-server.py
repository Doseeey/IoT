from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import socket
import time

key_size = 2048

start_key = time.time()
# Generate RSA key pair for the server
private_key_server = rsa.generate_private_key(
    public_exponent=65537,
    key_size=key_size,
    backend=default_backend()
)
public_key_server = private_key_server.public_key()

# Serialize server public key
server_public_key_pem = public_key_server.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
end_key = time.time()
# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)
print("Server is listening...")

# Accept client connection
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

# Send server public key to the client
client_socket.sendall(server_public_key_pem)

start_decrypt = time.time()
# Receive encrypted message from client and decrypt it using server private key
encrypted_message = client_socket.recv(4096)
plaintext_message = private_key_server.decrypt(
    encrypted_message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
).decode()

print("Received from client:", plaintext_message)
end_decrypt = time.time()

print(f"Time: {(end_key-start_key) + (end_decrypt-start_decrypt)}")
# Close sockets
client_socket.close()
server_socket.close()
