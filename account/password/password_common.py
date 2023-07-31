import re
from pathlib import Path

file = Path(__file__).resolve().parent / "common-passwords.txt"
try:
    with open(file) as f:
        password_list = {x.strip() for x in f}
except OSError:
    print("File not found")

def is_common_password(password):
    if password.lower().strip() in password_list:
        return True
    return False

def is_regex_validated(password):
    """ Check if password contains at least one number, 
    one uppercase letter, one lowercase letter and one special character """
    
    if not re.search(r"\w", password):
        # If the password does not contain any letters, return False
        return False
    
    if not re.search(r"[0-9]", password):
        # If the password does not contain any numbers, return False
        return False
    
    if not re.search(r"[!@#$%^&*()_+{}|:<>?~-]", password):
        # If the password does not contain any special characters, return False
        return False
    
    return True