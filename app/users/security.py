from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

def hash_password(password):
    ph = PasswordHasher()
    hash = ph.hash(password=password)
    return hash

def verify_hash(pwd_hash, pwd_raw):
    ph = PasswordHasher()
    verified = False
    msg = ""
    try:
        verified = ph.verify(pwd_hash, pwd_raw)
    except VerifyMismatchError:
        verified = False
        msg = "Invalid password."
    except Exception as e:
        verified = False
        msg = f"Unexpected error: {e}"

    return verified, msg
