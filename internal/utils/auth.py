from argon2.exceptions import VerifyMismatchError
from argon2 import PasswordHasher
import secrets


ph = PasswordHasher() 

# The argon2 hashing algo already adds 16-byte random salt
def hash_password(password, max_pass_length=128):
    if len(password) > max_pass_length:
        raise Exception(f"Can't hash password; length exceeds {max_pass_length}.")
    return ph.hash(password) 


def verify_hash(argon2_hash: str, password: str) -> bool:
    try:
        ph.verify(argon2_hash, password)
        return True
    except VerifyMismatchError:
        return False
    
    
def generate_session_id(length_bytes=16):
    # According to OWASP, a session ID must be at least 16 hexadecimal char to achieve 64 bits of entropy
    return secrets.token_urlsafe(length_bytes)


if __name__ == "__main__":
    password = input("Password:")

    hashed = hash_password(password)
    print("Hashed Password:", hashed)

    while True:
        verify = input("Verify:")
        if verify_hash(hashed, verify):
            print("Verified")
            break
        print("Wrong password")