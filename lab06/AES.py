import random
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# Large prime number (p) and primitive root (g)
p = 23  # Example small prime number
g = 5   # Example small primitive root modulo p

def generate_private_key(p):
    return random.randint(2, p-2)

def generate_public_key(private_key, g, p):
    return pow(g, private_key, p)

def compute_shared_secret(received_public_key, private_key, p):
    return pow(received_public_key, private_key, p)

# Alice generates her private and public keys
alice_private_key = generate_private_key(p)
alice_public_key = generate_public_key(alice_private_key, g, p)

# Bob generates his private and public keys
bob_private_key = generate_private_key(p)
bob_public_key = generate_public_key(bob_private_key, g, p)

# Alice and Bob exchange public keys and compute the shared secret
alice_shared_secret = compute_shared_secret(bob_public_key, alice_private_key, p)
bob_shared_secret = compute_shared_secret(alice_public_key, bob_private_key, p)

# Verify that both shared secrets are the same
assert alice_shared_secret == bob_shared_secret

# Optionally, hash the shared secret for use as a symmetric key
shared_secret_hash = hashlib.sha256(str(alice_shared_secret).encode()).digest()
aes_key = shared_secret_hash[:32]  # Use the first 32 bytes (256 bits) for AES-256

def encrypt(plaintext, key):
    iv = os.urandom(16)  # Generate a random 16-byte IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the plaintext to be a multiple of the block size (16 bytes)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return iv + ciphertext  # Prepend the IV to the ciphertext

def decrypt(ciphertext, key):
    iv = ciphertext[:16]  # Extract the IV from the beginning of the ciphertext
    actual_ciphertext = ciphertext[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

    # Unpad the plaintext
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext

# Example plaintext
plaintext = b'This is a secret message.'

# Encrypt the plaintext
ciphertext = encrypt(plaintext, aes_key)
print(f'Ciphertext: {ciphertext}')

# Decrypt the ciphertext
decrypted_plaintext = decrypt(ciphertext, aes_key)
print(f'Decrypted Plaintext: {decrypted_plaintext}')
