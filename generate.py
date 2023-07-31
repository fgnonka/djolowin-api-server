import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

# Function to generate the encryption key
def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = kdf.derive(password)
    return key

# Generate a random salt
salt = os.urandom(16)

# Replace "your_password_here" with a strong password
password = b"eFBa6ehl1cer9p_qYsMArV4DsS7Ne0IrdLX9ZxSyWsg="

# Generate the encryption key
encryption_key = generate_key(password, salt)

# Convert the encryption key to a base64-encoded string
encoded_encryption_key = base64.urlsafe_b64encode(encryption_key).decode()

# Save the encoded encryption key to a secure location (e.g., environment variable, configuration file)
# Make sure to keep the key secret and not share it with others
print("Encoded Encryption Key:", encoded_encryption_key)
