from argon2.exceptions import VerifyMismatchError
from argon2 import PasswordHasher

ph = PasswordHasher() 

# The argon2 hashing algo already adds 16-byte random salt
def hash_password(password, max_pass_length=128):
    if len(password) > max_pass_length:
        raise Exception(f"Can't hash password; length exceeds {max_pass_length}.")
    return ph.hash(password) 

def verify_hash(salted_hash: str, salted_password: str) -> bool:
    try:
        ph.verify(salted_hash, salted_password)
        return True
    except VerifyMismatchError:
        return False


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