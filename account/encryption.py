import base64
import hmac
import hashlib

from django.conf import settings
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Generate a new encryption key
# This should be generated only once and kept securely (e.g., in Django settings)
ENCRYPTION_KEY = settings.ENCRYPT_KEY

def encrypt_token(token):
    # Convert the token to bytes
    token_bytes = token.encode()
    encoded_key = ENCRYPTION_KEY.encode()
    # Generate an HMAC-SHA256 signature using the secret key
    signature = hmac.new(encoded_key, token_bytes, hashlib.sha256).digest()

    # Combine the token and signature
    combined_token = token_bytes + signature

    # Base64 encode the combined token
    encoded_token = base64.urlsafe_b64encode(combined_token)

    # Convert the bytes to a string
    return encoded_token.decode()


def decrypt_token(encoded_token):
    # Convert the encoded token string to bytes
    encoded_token_bytes = encoded_token.encode()

    # Base64 decode the token bytes
    combined_token = base64.urlsafe_b64decode(encoded_token_bytes)

    # Split the combined token into the original token and signature
    token_bytes = combined_token[:-32]  # The last 32 bytes are the signature
    signature = combined_token[-32:]
    encoded_key = ENCRYPTION_KEY.encode()

    # Verify the signature using the secret key
    expected_signature = hmac.new(encoded_key, token_bytes, hashlib.sha256).digest()
    if hmac.compare_digest(signature, expected_signature):
        # Signature is valid, return the decoded token
        return token_bytes.decode()
    else:
        # Signature is not valid, token may have been tampered with
        return None
