import bcrypt

def hash_password(plain_password: str) -> str:
    hashed_password = bcrypt.hashpw(
        plain_password.encode(),
        bcrypt.gensalt()
    )
    return hashed_password.decode()

def verify_password(
        password: str,
        hashed_password: str
)-> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )